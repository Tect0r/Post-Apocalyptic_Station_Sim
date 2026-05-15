from metro_sim.player.factories.player_factory import create_initial_player


def test_initial_player_has_individual_crew_members():
    player = create_initial_player()

    assert len(player.crew.crew_members) == 6
    assert player.crew.members == 6


def test_initial_crew_members_have_roles_and_skills():
    player = create_initial_player()
    member = player.crew.crew_members[0]

    assert member.id is not None
    assert member.name is not None
    assert member.role is not None
    assert "scouting" in member.skills
    assert "combat" in member.skills