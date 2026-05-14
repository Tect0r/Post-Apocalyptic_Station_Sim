import type { WorldEvent } from "../../types/game";

type EventListProps = {
  events: WorldEvent[];
};

export function EventList({ events }: EventListProps) {
  return (
    <section className="panel" id="events">
      <h2>Events</h2>

      {events.length === 0 ? (
        <p className="muted">No events yet.</p>
      ) : (
        <div className="list-grid">
          {events.map((event) => (
            <div className="event-row" key={event.id}>
              <div>
                <strong>{event.event_type}</strong>
                <p>{event.description_key}</p>
              </div>
              <span>Tick {event.tick}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}