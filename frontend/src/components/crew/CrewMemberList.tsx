import type { CrewMember } from "../../types/game";

type CrewMemberListProps = {
  crewMembers: CrewMember[];
};

export function CrewMemberList({ crewMembers }: CrewMemberListProps) {
  return (
    <section className="panel">
      <h2>Crew Members</h2>

      <div className="card-list">
        {crewMembers.map((member) => (
          <div className="route-card" key={member.id}>
            <strong>{member.name}</strong>
            <span>Role: {member.role}</span>
            <span>Status: {member.status}</span>
            <span>Location: {member.current_location_id}</span>
            <span>Health: {member.health}</span>
            <span>Morale: {member.morale}</span>
            <span>Fatigue: {member.fatigue}</span>
            <span>
              Skills:{" "}
              {Object.entries(member.skills)
                .map(([skill, value]) => `${skill}: ${value}`)
                .join(", ")}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}