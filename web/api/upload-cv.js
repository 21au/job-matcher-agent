import formidable from 'formidable'
import fs from 'fs'
import pdf from 'pdf-parse'
import { createClient } from '@supabase/supabase-js'

export const config = {
  api: { bodyParser: false },
}

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY)

async function callGroq(prompt) {
  const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GROQ_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'llama-3.3-70b-versatile',
      temperature: 0,
      messages: [{ role: 'user', content: prompt }],
    }),
  })
  const data = await res.json()
  let text = data.choices?.[0]?.message?.content?.trim() || ''
  text = text.replace(/```json/g, '').replace(/```/g, '').trim()
  return JSON.parse(text)
}

async function parseCV(cvText) {
  const prompt = `Kamu adalah CV Parser Specialist. Ubah teks mentah CV menjadi data terstruktur JSON.
Ekstrak: name, email, skills (list), experience (list), education (list).
PENTING: Balas HANYA dengan JSON valid, tanpa teks tambahan.

Teks CV:
${cvText}`
  return await callGroq(prompt)
}

async function matchToJob(cvData, job) {
  const prompt = `Kamu adalah CV-Job Matcher. Bandingkan skill kandidat dengan lowongan berikut.

CV: Skills: ${cvData.skills?.join(', ')}. Experience: ${cvData.experience?.join(', ')}.

LOWONGAN:
Judul: ${job.title}
Deskripsi: ${(job.description || '').slice(0, 1200)}

Balas HANYA JSON: {"score": 0-100, "matched_skills": [], "missing_skills": [], "summary": "..."}`
  return await callGroq(prompt)
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const form = formidable({})
    const [fields, files] = await form.parse(req)

    const file = files.cv?.[0]
    if (!file) return res.status(400).json({ error: 'File CV tidak ditemukan' })

    const dataBuffer = fs.readFileSync(file.filepath)
    const pdfData = await pdf(dataBuffer)
    const cvText = pdfData.text

    const cvData = await parseCV(cvText)

    // Ambil beberapa lowongan terbaru buat di-match (dibatasi biar hemat kuota)
    const { data: jobs } = await supabase
      .from('job_postings')
      .select('*')
      .order('fetched_at', { ascending: false })
      .limit(8)

    const matches = []
    for (const job of jobs || []) {
      const match = await matchToJob(cvData, job)
      matches.push({ job, match })
    }
    matches.sort((a, b) => b.match.score - a.match.score)

    // Mode "CV Saya" — simpan sebagai CV aktif kalau password benar
    const setAsPrimary = fields.setPrimary?.[0] === 'true'
    const password = fields.password?.[0]
    let savedAsPrimary = false

    if (setAsPrimary && password === process.env.PERSONAL_CV_SECRET) {
      await supabase.from('cvs').insert({
        name: cvData.name,
        email: cvData.email,
        skills: cvData.skills || [],
        experience: cvData.experience || [],
        education: cvData.education || [],
        raw_text: cvText,
      })
      savedAsPrimary = true
    }

    return res.status(200).json({ cvData, matches, savedAsPrimary })
  } catch (err) {
    console.error(err)
    return res.status(500).json({ error: err.message })
  }
}