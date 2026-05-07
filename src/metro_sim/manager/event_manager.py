import metro_sim.utils.file_loader as loader

def random_event_refugees(station:dict) -> dict:
    #check moral, security and comfort
    # calculate the amount of refugees
    # calculate the refugees that want to join
    #optionen zum annehmen oder abweisen
    #   abweisen verringert moral
    #   annehmen erhöht moral und verringert sicherheit und komfort
    #build dict to return
    return {}

def random_event_power_outage(station: dict) -> None:
    #zufällige chance, abhängig vom vertrag und vom benutzten power
    # wenn zutrifft, zufällige anzahl von ticks fehlt der komplette strom oder nur ein teil
    # abhängig davon, wieviel strom fehlt, geht komfort und moral runter
    pass

def random_event_water_contermination() -> None:
    #random chance, abhängig von der maitenance, dass das wasser konterminiert wird und für eine random anzahl
    # von ticks nicht mehr genutzt werden kann
    # option wasser weiter zu benutzen -> erhöht chance auf krankheit
    pass