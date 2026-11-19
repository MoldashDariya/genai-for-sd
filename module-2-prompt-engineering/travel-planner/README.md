# Travel Planner

**Task:** use an AI assistant to plan a three-day trip to Barcelona with the most suitable prompting technique(s).
The plan must be balanced (historical, cultural and outdoor attractions), list cafes and restaurants near each day's
attractions, and recommend transportation between attractions.

**Score:** 100 / 100 (1st attempt)

**Technique:** role prompting + explicit instructions and constraints + a structured output template
(reviewer: zero-shot with Directional Stimulus Prompting).

## Submitted solution

```text
1. Solution summary:
To solve the task, I applied the role prompting technique (the AI acts as an experienced local Barcelona travel guide) combined with explicit instructions, constraints and a structured output template, so that every acceptance criterion (balanced mix of historical, cultural and outdoor attractions, nearby cafes and restaurants for each day, transportation between attractions) is stated directly in the prompt and cannot be skipped. In total, I created 1 prompt - it defines the role, the context (3-day trip to Barcelona), the requirements and the exact day-by-day output format. Clustering each day's attractions by neighbourhood was requested so that food recommendations and transport tips stay realistic and close to the sights.

2. Finalized solution:

Prompt:
You are an experienced local travel guide in Barcelona who creates practical, well-balanced itineraries for first-time visitors.
Create a detailed 3-day travel plan for Barcelona.
Requirements:
- The trip must be balanced: every day must include a mix of historical sights, cultural attractions (museums, architecture, art) and outdoor activities (parks, viewpoints, beach).
- Group each day's attractions by neighbourhood so that they are close to each other and the route is logical.
- For each day, list 2-3 suitable cafes and restaurants located near that day's attractions (name, area, what it is good for).
- For each move between attractions, give a transportation recommendation (walking, metro line and station, bus, funicular or cable car) with approximate travel time.
- Add short practical tips (tickets to book in advance, best time to visit).
Output format (use it for every day):
Day N - <theme / area>
Morning: <attraction> (<type: historical / cultural / outdoor>) - short description
-> Transport: <how to get to the next stop, time>
Afternoon: ...
-> Transport: ...
Evening: ...
Where to eat: <cafes and restaurants near the day's attractions>
Tips: ...
Finish with a short "General tips" section (transport pass, tickets).

Output:
Day 1 - Gothic Quarter, El Born and the seaside
Morning: Barcelona Cathedral and the Gothic Quarter (historical) - walk the medieval streets, Placa del Rei and the Roman walls; visit the MUHBA History Museum with Roman ruins underground.
-> Transport: walk 10 min to El Born.
Late morning: Picasso Museum (cultural) - collection of Picasso's early works in medieval palaces on Carrer Montcada; see the Santa Maria del Mar basilica nearby (historical).
-> Transport: walk 10 min.
Afternoon: Parc de la Ciutadella (outdoor) - the Cascada fountain, the lake with rowing boats, Arc de Triomf.
-> Transport: walk 20 min or metro L4 from Ciutadella | Vila Olimpica to Barceloneta (5 min).
Evening: Barceloneta beach and seafront promenade (outdoor) - sunset walk along the sea.
Where to eat: Caelum (Gothic Quarter, cafe with cakes in a medieval cellar); Satan's Coffee Corner (Gothic Quarter, specialty coffee); El Xampanyet (El Born, classic cava and tapas bar); La Cova Fumada (Barceloneta, the original "bomba" and grilled seafood); Can Sole (Barceloneta, seafood paella for dinner).
Tips: the Gothic Quarter is best explored on foot in the morning before the crowds; the Picasso Museum is free on Thursday evenings and the first Sunday of the month (book online).

Day 2 - Gaudi and Modernisme (Eixample and Gracia)
Morning: Sagrada Familia (historical / cultural) - Gaudi's basilica, book a timed ticket with tower access in advance.
-> Transport: metro L5 from Sagrada Familia to Diagonal (5 min).
Late morning: Casa Batllo and Casa Mila (La Pedrera) on Passeig de Gracia (cultural) - Modernist houses with rooftop terraces.
-> Transport: walk 15 min through Gracia, or metro L3 Diagonal -> Lesseps (5 min) + 15 min walk uphill (or bus V19 / 24 closer to the entrance).
Afternoon: Park Guell (outdoor / cultural) - mosaic terrace, gardens and panoramic city views; continue to Bunkers del Carmel for a free sunset viewpoint (25 min walk or bus V17).
-> Transport: walk downhill 20 min to Vila de Gracia.
Evening: stroll through the squares of Gracia (Placa del Sol, Placa de la Virreina).
Where to eat: Granja Petitbo (Eixample, brunch and coffee); Cerveceria Catalana (Eixample, near Passeig de Gracia, popular tapas); La Pubilla (Gracia, traditional Catalan lunch menu); Bar Bodega Quimet (Gracia, vermouth and tapas for dinner).
Tips: Sagrada Familia, Casa Batllo and Park Guell all require timed tickets - book 1-2 weeks ahead; visit Park Guell late afternoon for softer light.

Day 3 - Montjuic hill, art and the Magic Fountain
Morning: Funicular to Montjuic and Fundacio Joan Miro (cultural) - modern art museum with terraces and city views.
-> Transport: metro L2/L3 to Paral-lel, then the Montjuic funicular (included in a regular metro ticket, 2 min) + 5 min walk.
Late morning: Montjuic Castle (historical) - 17th-century fortress with views over the port.
-> Transport: Teleferic de Montjuic cable car up to the castle (5 min), then walk back down through the gardens.
Afternoon: Montjuic gardens - Jardins de Mossen Costa i Llobera / Laribal (outdoor), then MNAC - National Art Museum of Catalonia (cultural, Romanesque frescoes) in the Palau Nacional.
-> Transport: walk 15 min downhill (outdoor escalators) to Placa d'Espanya area.
Evening: Magic Fountain of Montjuic (cultural / outdoor) - light and music show (check the seasonal schedule), then walk 10 min to Poble-sec for dinner.
Where to eat: Federal Cafe (Sant Antoni, near Paral-lel, breakfast); Quimet & Quimet (Poble-sec, famous montaditos and conservas); Bar Seco (Poble-sec, relaxed lunch); pintxos bars on Carrer de Blai (Poble-sec, dinner).
Tips: wear comfortable shoes - Montjuic involves a lot of walking; MNAC is free on Saturdays after 15:00 and the first Sunday of the month.

General tips:
- Buy a T-casual card (10 metro/bus/funicular trips) or the Hola Barcelona travel card for 72 hours - it covers metro, buses and the Montjuic funicular.
- Book Sagrada Familia, Casa Batllo, Park Guell and the Picasso Museum online in advance.
- Lunch in Barcelona is usually 13:30-15:30 and dinner after 20:30; look for the "menu del dia" for a good-value lunch.
```
