from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from models import *
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Добавляем зависимости
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получение списка атлетов
@app.get("/get_athletes", response_class=HTMLResponse)
async def get_athletes(request: Request, db: Session = Depends(get_db)):
    athletes = db.query(Athlete).all()
    context = {"athletes": athletes}
    return templates.TemplateResponse(
        request=request, name="athletes.html", context=context
    )


# Добавление спортсмена
@app.post("/add_athlete/")
def add_athlete(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    db: Session = Depends(get_db),
):
    new_athlete = Athlete(name=name, age=age)
    db.add(new_athlete)
    db.commit()
    return RedirectResponse(url=request.url_for("get_athletes"), status_code=303)


# Удаление спортсмена
@app.post("/delete_athlete/{athlete_id}")
def delete_athlete(request: Request, athlete_id: int, db: Session = Depends(get_db)):
    athlete_to_delete = db.query(Athlete).filter(Athlete.id == athlete_id).first()
    db.delete(athlete_to_delete)
    db.commit()
    return RedirectResponse(url=request.url_for("get_athletes"), status_code=303)


# Получение списка соревнований
@app.get("/get_competitions", response_class=HTMLResponse)
def get_competitions(request: Request, db: Session = Depends(get_db)):
    competitions = db.query(Competition).all()
    context = {"competitions": competitions}
    return templates.TemplateResponse(
        name="competitions.html", request=request, context=context
    )


# Добавление соревнования
@app.post("/add_competition")
def add_competition(
    request: Request,
    title: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db),
):
    new_competition = Competition(title=title, date=date)
    db.add(new_competition)
    db.commit()
    return RedirectResponse(url=request.url_for("get_competitions"), status_code=303)


# Удаление соревнования
@app.post("/delete_competition/{id}")
def delete_competition(request: Request, comp_id: int, db: Session = Depends(get_db)):
    competition_to_delete = (
        db.query(Competition).filter(Competition.id == comp_id).first()
    )
    if competition_to_delete:
        db.delete(competition_to_delete)
        db.commit()
    return RedirectResponse(url=request.url_for("get_competitions"), status_code=303)


# Добавление участия
@app.post("/add_participation")
def add_participation(
    request: Request,
    athlete_id: int = Form(...),
    competition_id: int = Form(...),
    db: Session = Depends(get_db),
):
    new_participation = Participation(
        athlete_id=athlete_id, competition_id=competition_id
    )
    db.add(new_participation)
    db.commit()
    return RedirectResponse(url=request.url_for("get_participations"), status_code=303)


# Удаление участников
@app.post("/delete_participation/{athlete_id}/{competition_id}")
def delete_participation(
    request: Request,
    athlete_id: int,
    competition_id: int,
    db: Session = Depends(get_db),
):
    participation_to_delete = (
        db.query(Participation)
        .filter(
            Participation.athlete_id == athlete_id,
            Participation.competition_id == competition_id,
        )
        .first()
    )
    if participation_to_delete:
        db.delete(participation_to_delete)
        db.commit()
        return RedirectResponse(
            url=request.url_for("get_participations"), status_code=303
        )


# Получение списка участников
@app.get("/get_participations", response_class=HTMLResponse)
def get_participations(request: Request, db: Session = Depends(get_db)):
    participations = db.query(Participation).all()
    context = {"participations": participations}
    return templates.TemplateResponse(
        name="participations.html", request=request, context=context
    )
