from metro_sim.services import time_service
import metro_sim.utils.file_loader as loader
import metro_sim.services.production_service as production_service
import metro_sim.services.consumption_service as consumption_service
import metro_sim.services.report_service as report_service


def calculate_next_tick(station: dict, report: dict) -> dict:
    # Berechnet die Ereignisse des nächsten Ticks und aktualisiert den Stationsstatus entsprechend
    time_service.advance_time(station, 1)
    balancing_dict = loader.load_balancing()

    if station["time"]["hour"] >= balancing_dict["time"]["work_start_hour"] and station["time"]["hour"] <= balancing_dict["time"]["work_end_hour"]:
        production_report = production_service.calculate_production_for_tick(station)
        report_service.merge_reports(report, production_report)

    consumption_report = consumption_service.calculate_consumption_for_tick(station)
        
    report_service.merge_reports(report, consumption_report)




