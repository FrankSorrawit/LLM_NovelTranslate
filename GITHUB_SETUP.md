# การตั้งค่า GitHub Repository / GitHub Repository Setup

## ขั้นตอนการอัปโหลดไปยัง GitHub / Steps to Upload to GitHub

### 1. เตรียมไฟล์ / Prepare Files
```bash
# รันสคริปต์ตั้งค่า Git / Run Git setup script
setup_git.bat
```

### 2. สร้าง Repository ใหม่บน GitHub / Create New Repository on GitHub
1. ไปที่ https://github.com และล็อกอิน / Go to https://github.com and login
2. คลิก "New repository" / Click "New repository"
3. ตั้งชื่อ repository เช่น `thai-novel-translator` / Name your repository like `thai-novel-translator`
4. เลือก Public หรือ Private ตามต้องการ / Choose Public or Private as desired
5. **อย่า** เลือก "Initialize with README" / **Don't** select "Initialize with README"
6. คลิก "Create repository" / Click "Create repository"

### 3. เชื่อมต่อและอัปโหลด / Connect and Upload
```bash
# เชื่อมต่อกับ GitHub repository / Connect to GitHub repository
git remote add origin https://github.com/[USERNAME]/[REPOSITORY-NAME].git

# ตั้งชื่อ branch หลักเป็น main / Set main branch name to main
git branch -M main

# อัปโหลดไฟล์ทั้งหมด / Upload all files
git push -u origin main
```

### ตัวอย่าง / Example:
```bash
git remote add origin https://github.com/bloodstormm/thai-novel-translator.git
git branch -M main
git push -u origin main
```

## การอัปเดตในอนาคต / Future Updates

### เมื่อมีการเปลี่ยนแปลงไฟล์ / When you have file changes:
```bash
# เพิ่มไฟล์ที่เปลี่ยนแปลง / Add changed files
git add .

# สร้าง commit พร้อมข้อความ / Create commit with message
git commit -m "อัปเดต: [อธิบายการเปลี่ยนแปลง] / Update: [describe changes]"

# อัปโหลดการเปลี่ยนแปลง / Upload changes
git push
```

## ไฟล์ที่จะถูกอัปโหลด / Files That Will Be Uploaded

### ✅ ไฟล์ที่รวมอยู่ / Included Files:
- 📄 `README.md` - คำอธิบายโครงการ (ไทย/อังกฤษ) / Project description (Thai/English)
- 🔧 `dual_novel_translator.py` - ระบบแปลหลัก / Main translation system
- 📋 `thai_pdf_fixer.py` - สร้าง PDF ภาษาไทย / Thai PDF creator
- ⚙️ `config.json` - การตั้งค่า / Configuration
- 📚 `Raw/` - นิยายต้นฉบับ / Original novels
- 📄 **เฉพาะ PDF ผลลัพธ์สุดท้าย** / **Only final result PDFs**
- 🎯 สคริปต์และไฟล์สำคัญอื่นๆ / Other important scripts and files

### ❌ ไฟล์ที่ไม่รวม (ตาม .gitignore) / Excluded Files (per .gitignore):
- 🗂️ `__pycache__/` - ไฟล์ Python ชั่วคราว / Temporary Python files
- 📊 `*_progress.json` - ไฟล์ความคืบหน้าชั่วคราว / Temporary progress files
- 🔐 ไฟล์ API key และความลับ / API keys and secrets
- 📝 **ไฟล์ข้อความที่แปลแล้วทั้งหมด** / **All translated text files**
- 📁 `FINAL_THAI_TRANSLATIONS/` - ไฟล์ขนาดใหญ่ในโฟลเดอร์ / Large files in organized folder
- 💾 ไฟล์ขนาดใหญ่อื่นๆ / Other large files

### 📄 PDF Files - เฉพาะผลลัพธ์สุดท้าย / Only Final Results:
- ✅ `matriarch_thai_font.pdf` - รวมอยู่ (ไฟล์ผลลัพธ์สำคัญเท่านั้น) / Included (important result file only)
- ✅ `viridescent_thai_font.pdf` - รวมอยู่ (ไฟล์ผลลัพธ์สำคัญเท่านั้น) / Included (important result file only)

## เคล็ดลับ / Tips

1. **ตรวจสอบขนาดไฟล์** / **Check file sizes**: GitHub มีขีดจำกัด 100MB ต่อไฟล์ / GitHub has a 100MB per file limit
2. **ใช้ Git LFS** สำหรับไฟล์ขนาดใหญ่หากจำเป็น / **Use Git LFS** for large files if needed
3. **อัปเดตเป็นประจำ** / **Update regularly**: commit และ push การเปลี่ยนแปลงเป็นประจำ / commit and push changes regularly
4. **เขียนข้อความ commit ที่ชัดเจน** / **Write clear commit messages**: อธิบายการเปลี่ยนแปลงอย่างชัดเจน / describe changes clearly

## การแก้ไขปัญหา / Troubleshooting

### ถ้าไฟล์ใหญ่เกินไป / If files are too large:
```bash
# ตรวจสอบขนาดไฟล์ / Check file sizes
git ls-files -s | sort -k2 -nr | head -10

# ลบไฟล์ขนาดใหญ่ออกจาก Git / Remove large files from Git
git rm --cached [filename]
git commit -m "Remove large file"
```

### ถ้ามีปัญหาการ push / If having push issues:
```bash
# ดึงการเปลี่ยนแปลงล่าสุดก่อน / Pull latest changes first
git pull origin main

# แล้วลอง push อีกครั้ง / Then try pushing again
git push
```