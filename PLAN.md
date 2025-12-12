# Journey Plan (agent output shape)
- Origin: ____________________ | Destination: ____________________
- Data sources: aggregate ~20 sites (Makemytrip, Cleartrip, TripAdvisor + OTAs/meta/activity portals) for routes, fares, stays, and highlights; fall back to cached samples when offline.
- Minimal input: start/end + date; agent should ask only for essentials and infer defaults.
- Departure: transport mode, date/time, tickets/visa, baggage rules
- Arrival & transfer: airport/station to accommodation, check-in window, backup options
- Daily outline: day-by-day highlights, buffers, meals; mark paid/free items
- Local transport: passes/tickets, ride-share, parking
- Return: checkout timing, transfer back, departure buffer
- Notes: constraints, accessibility, contingency options
