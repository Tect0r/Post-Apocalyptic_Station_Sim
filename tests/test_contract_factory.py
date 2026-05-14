from metro_sim.world.factories.world_factory import create_world


def test_world_loads_contracts():
    world = create_world()

    assert len(world.contracts) > 0
    assert "contract_support_paveletskaya_militia" in world.contracts


def test_loaded_contract_has_expected_fields():
    world = create_world()
    contract = world.contracts["contract_support_paveletskaya_militia"]

    assert contract.title == "Support Paveletskaya Militia"
    assert contract.target_id == "paveletskaya"
    assert contract.action_type == "support_militia"
    assert contract.duration_ticks > 0