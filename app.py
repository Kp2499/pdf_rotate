import PyPDF2 
import time
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)
def PDFrotate(origFileName, newFileName, rotation, tgt_pages):
    pdfFileObj = open('static//'+origFileName, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfWriter = PyPDF2.PdfFileWriter()
     
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        if page in tgt_pages:
          pageObj.rotateClockwise(rotation)
        pdfWriter.addPage(pageObj)
    newFile = open(newFileName, 'wb')
    pdfWriter.write(newFile)
    pdfFileObj.close()

    newFile.close()


app.config['UPLOAD_FOLDER'] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
      pdf_file = request.files['file']
      rotation = int(request.form.get("rotation"))
      tgt_pages = [int(x)-1 for x in request.form.get("tgt_pages").split(',')]

      filename = secure_filename(pdf_file.filename)
      pdf_file.save(app.config['UPLOAD_FOLDER'] + filename)

      origFileName = filename
      # new pdf file name
      newFileName = 'rotated_' + origFileName
      PDFrotate(origFileName, newFileName, rotation, tgt_pages)
      time.sleep(2)
    return send_file('./'+newFileName,as_attachment=True)


if __name__=='__main__'  :
  app.run()
      