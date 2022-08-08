#!/usr/bin/python
# author: David ML

import datetime
import re
import uvicorn

from app.models import Employee
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

NIF_CODIFICATION = "TRWAGMYFPDXBNJZSQVHLCK"
app = FastAPI()
employee_pydantic = pydantic_model_creator(Employee, name='Employee')
employee_in_pydantic = pydantic_model_creator(Employee, name='EmployeeIn', exclude_readonly=True)


@app.get("/")
async def read_root():
    return {"Hello": "World of Employee"}


def valid_employee(employee: employee_in_pydantic):
    # EMAIL VALIDATION
    if not re.match(r"^[a-zA-Z\d\-_]+@[a-zA-Z\d]+\.[a-z]{1,3}$", employee.email):
        raise HTTPException(400, f"Invalid Email: {employee.email} its not a valid email")

    # NIF VALIDATION: Correct len
    if len(employee.nif) != 9:
        raise HTTPException(400, f"Invalid NIF: {employee.nif} its not a valid NIF cause doesnt have correct length")
    # NIF VALIDATION: Correct structure (12345678A or X1234567A)
    if not re.match(r"^[X-Z\d]\d{7}[A-Z]$", employee.nif):
        raise HTTPException(400, f"Invalid NIF: {employee.nif} its not a valid NIF.")
    # NIF VALIDATION: Correct final letter (12345678A or X1234567A)
    if not NIF_CODIFICATION[(int(re.search(r'\d+', employee.nif).group()) % 23)] == employee.nif[-1]:
        raise HTTPException(400, f"Invalid NIF: {employee.nif} does not have valid letter")
    # NIF VALIDATION: Unique NIF
    # if Employee.filter(nif=employee.nif):
    # if employee_pydantic.from_queryset_single(Employee.get(id=employee.nif)):
    #     raise HTTPException(400, f"Invalid NIF: {employee.nif} exists yet on our db")

    # DATE VALIDATION: Correct date > today (always future incorporations)
    if employee.fecha_incorporacion <= datetime.date.today():
        raise HTTPException(400, f"Invalid Date: {employee.fecha_incorporacion} migth be tomorrow or later")


@app.post("/employee/create/", response_model=employee_pydantic)
async def create_employee(employee: employee_in_pydantic):
    # employee.nif = employee.nif.upper()
    valid_employee(employee)

    json = employee.dict(exclude_unset=True)

    # json['fecha_incorporacion'] = datetime.datetime.now()

    job = await Employee.create(**json)
    return await employee_pydantic.from_tortoise_orm(job)


@app.get("/employee/{employee_id}", response_model=employee_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_employee(employee_id: int):
    return await employee_pydantic.from_queryset_single(Employee.get(id=employee_id))


@app.get("/employees/")
async def get_employees():
    return await employee_pydantic.from_queryset(Employee.all())


@app.put("/employee/{employee_id}", response_model=employee_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_employee(employee_id: int, employee: employee_in_pydantic):
    await Employee.filter(id=employee_id).update(**employee.dict())
    return await employee_pydantic.from_queryset_single(Employee.get(id=employee_id))


@app.delete("/employee/{employee_id}", response_model=str, responses={404: {"model": HTTPNotFoundError}})
async def delete_employee(employee_id: int):
    deleted_employee = await Employee.filter(id=employee_id).delete()
    if not deleted_employee:
        return f"Employee {employee_id} not found"
    return f"Deleted employee {employee_id}"


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


def main():
    uvicorn.run(app, host="127.0.0.3", port=8088)


if __name__ == "__main__":
    main()
