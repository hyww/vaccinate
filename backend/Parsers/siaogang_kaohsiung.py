from typing import Tuple
import requests
from bs4 import BeautifulSoup
from hospital_types import (
    HospitalID,
    AppointmentAvailability,
    ScrapedData,
    HospitalAvailabilitySchema,
)


def parse_siaogang_kaohsiung() -> ScrapedData:
    def has_no_appointments(option: BeautifulSoup) -> bool:
        option = option.text
        return int(option[option.find("數") + 2 :].split("-")[0]) == 0

    r = requests.get(
        "https://www.kmsh.org.tw/web/BookVaccineSysInter",
        timeout=2,
    )
    soup = BeautifulSoup(r.text, "html.parser")
    select = soup.find("select", {"id": "InputBookDate"})
    options = select.find_all("option")
    options = list(filter(has_no_appointments, options))

    availability: HospitalAvailabilitySchema = {
        "self_paid": AppointmentAvailability.AVAILABLE
        if bool(options)
        else AppointmentAvailability.UNAVAILABLE,
        "government_paid": AppointmentAvailability.NO_DATA,
    }

    # PEP8 Style: if list is not empty, then there are appointments
    return (
        23,
        availability,
    )
