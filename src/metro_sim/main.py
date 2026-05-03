from metro_sim.services.state_factory import create_initial_station

def main():
    station = create_initial_station()
    print(station["resources"]["food"])
    print(station["population"]["total"])
    print(station["work_assignment"]["guards"]) 


if __name__ == "__main__":
    main()