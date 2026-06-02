from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas, utils, ml

models.Base.metadata.create_all(bind=database.engine)
print("Registered tables:", models.Base.metadata.tables.keys())
models.Base.metadata.create_all(bind=database.engine)
print("Tables created successfully")

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = "",
    db: Session = Depends(get_db)
):
    content = utils.extract_text_from_pdf(file.file)

    score = ml.calculate_score(content, job_description)

    resume = models.Resume(
        filename=file.filename,
        content=content,
        score=score
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"id": resume.id, "score": score}