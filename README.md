# Serene Screens Wallpapers

Desktop wallpapers that pair with each scene in [Serene Screens](https://github.com/dsreinhart/Stormy-Weather),
served to the app over GitHub Pages. The app reads `manifest.json`, shows the
thumbnail for the selected scene, and downloads the full image on request.

Published at `https://dsreinhart.github.io/serene-screens-wallpapers/`.

## Layout

| Path | Contents |
|---|---|
| `images/<scene>.jpg` | Full-size wallpaper, 5120 × 3200 JPEG |
| `thumbs/<scene>.jpg` | 480 × 300 thumbnail, generated |
| `manifest.json` | What the app fetches, generated |
| `tools/make_placeholders.py` | Seeds `images/` with gradient placeholders |
| `tools/build_manifest.py` | Rebuilds `thumbs/` and `manifest.json` from `images/` |

`<scene>` is the scene's identifier in the app (`ParticleType` case name),
for example `cherryBlossoms`, `snow2`, `batsAndGhosts`. The full list is in
`tools/make_placeholders.py`.

## Replacing a placeholder

1. Save the finished art as `images/<scene>.jpg`, 5120 × 3200, JPEG quality around 85.
   Aim for roughly 3 MB per image.
2. Run the manifest builder (needs `/usr/bin/python3`, which has Pillow):

   ```bash
   /usr/bin/python3 tools/build_manifest.py
   ```

3. Commit and push. The app picks up the change the next time Settings opens.

Placeholders are tagged with a JPEG comment, so `placeholder` in the manifest
flips to `false` on its own once real art replaces them.

## Image guidelines

- **Leave the subject out.** The app animates the snow, fish, lanterns and so on.
  A wallpaper that already contains them clashes with the moving ones.
- **Keep it calm.** Desktop icons and the particle layer both sit on top, so lean
  toward soft focus, wide empty areas and restrained contrast.
- Keep the busiest detail in the lower third where the Dock sits, and the top clear
  for the menu bar.
- Most generators output 1024 to 2048 px. Upscale to 5120 × 3200 before saving.

## Prompts

Append to every prompt: *wide 16:10 desktop wallpaper, painterly, soft focus, no
text, no people, uncluttered with large areas of quiet space.*

### Weather

| Scene | Prompt |
|---|---|
| snow | Hushed winter forest at dusk, snow-laden pines fading into pale blue haze, a lone warm cabin window far away, no falling snow |
| snow2 | Extreme close-up of a frosted window pane at night, bokeh of distant streetlights, deep depth of field, cool blues |
| blusterySnow | Windswept frozen lake under a heavy slate sky, bent grasses rimed with ice, horizon lost in white, no visible snowfall |
| rain | Quiet gray morning on a cobblestone street, wet stones reflecting shop lights, mist in the air, muted teal and amber |
| heavyRain | Dark overcast coastline from a covered porch, railing in the foreground, sea and sky merged in charcoal and deep blue |
| stormy | Brooding storm front over open prairie, towering anvil cloud, last slice of golden light on the grass, distant lightning glow but no bolt |
| fog | Still moorland at dawn, bare tree silhouettes dissolving into layered gray-green mist, nearly monochrome |

### Nature & Garden

| Scene | Prompt |
|---|---|
| leaves | Sunlit birch and maple grove in late October, golden canopy, leaf-strewn path, warm backlight, no leaves in the air |
| cherryBlossoms | Pink cherry trees in full bloom arching over a quiet Kyoto canal, pale spring sky, petals still on the branches |
| fireflies | Midsummer meadow at nightfall, deep indigo sky, dark treeline, faint moonlight on tall grass, no visible fireflies |
| dandelionSeeds | Sun-drenched hillside meadow in soft wind, bright wildflowers out of focus, lens flare, warm greens and yellows |
| butterflies | Overgrown cottage garden in high summer, lavender and foxgloves, dappled afternoon light, pastel palette |
| insects | Golden hour at a pond's edge, reeds and lily pads, warm light on still water, shallow focus |
| soapBubbles | Sunny backyard lawn from a child's eye view, bright blue sky, white picket fence, pure playful colors |
| embers | Campfire glow at night, dark pine silhouettes, warm orange light pooling on stones, sky above left empty |
| birds | Rolling coastal cliffs at sunrise, vast open sky in peach and lavender, calm sea below, horizon low in frame |

### Festive Lights

| Scene | Prompt |
|---|---|
| christmasLights | Snowy suburban street at night, dark house roofs and bare trees, warm windows glowing, unlit gutters and eaves ready for lights |
| christmasLights2 | Cozy night street in a small town, snow on sidewalks, lampposts in warm halos, dark empty sky above the rooftops |
| christmasTree | Living room at night by a dark fireplace, armchair, wrapped presents in shadow, open floor space where a tree would stand |
| christmasEve | Rooftops of a snow-covered village under a full moon, chimneys with curling smoke, deep navy sky, stars faint |
| stringLights | Mediterranean courtyard at twilight, terracotta walls, bistro tables, vines overhead, warm last light, no bulbs strung |
| chineseLanterns | Old Shanghai lane at night, dark tiled roofs and wooden shopfronts, wet stone street, deep red and ink black |
| skyLanterns | Wide river valley at night seen from a hilltop, distant town lights, mountains in silhouette, open starless sky |

### Sky

| Scene | Prompt |
|---|---|
| starryNight | Desert mesa under a moonless night, deep ink-black sky with only a faint Milky Way haze, no distinct stars |
| sunRays | Sunlit cathedral of old-growth redwoods, misty air, forest floor in shadow, warm amber light, no beams drawn |
| aurora | Frozen Arctic fjord at night, snow-capped peaks, mirror-still water, dark sky with only a faint green tint |
| shootingStars | Mountain lake under a dark summer sky, treeline silhouettes, faint reflections, empty sky with no stars |

### Seasonal & Fun

| Scene | Prompt |
|---|---|
| confetti | Empty party ballroom with polished floor and glowing stage lights, warm gold and magenta haze |
| hearts | Soft rose and blush gradient like silk, gentle bokeh, warm romantic glow |
| batsAndGhosts | Haunted hilltop manor under a huge orange moon, twisted bare trees, mist in the hollow, purple and black |
| fireworks | City skyline across a harbor at night, lights reflected in water, vast dark sky filling the upper two-thirds |
| balloons | Pastel summer sky over a rolling green fairground, striped tents far below, upper frame open and bright |
| musicNotes | Grand piano keys in soft focus, warm stage light, deep burgundy background with gentle vignette |
| shamrocks | Misty emerald hills of the Irish coast, stone walls, pale morning light, lush saturated greens |
| easterEggs | Spring meadow with tulips and a wicker basket, soft pastel light, gentle depth of field |
| paperPlanes | Sunny classroom window with wooden desks, chalkboard, dust in the light, open blue sky outside |
| umbrellas | Paris boulevard in gentle rain, wet pavement reflections, café awning, muted grays with pops of warm light |
| beachBalls | Bright tropical beach at noon, white sand, turquoise shallows, clear sky, towel and umbrella at the edge |
| lunarNewYear | Red lacquer temple gate with gold trim, hanging silk banners, warm festive glow, deep crimson and gold |
| champagne | Dark art-deco bar at midnight, brass and black marble, soft candlelight, deep gold and ebony |

### Under the Sea

| Scene | Prompt |
|---|---|
| jellyfish | Deep open ocean at twilight, soft blue-violet gradient, faint light rays from above, no sea life |
| schoolingFish | Sunlit coral reef with sandy floor, light caustics rippling, turquoise water, reef left and right with open water in the center |
| plankton | Midnight ocean seen from below the surface, near-black navy, faint moonlight shimmer on the surface above |
| kelp | Sunbeams filtering through green ocean water, rocky seabed, hazy depth, no kelp fronds drawn |
| bubbleStream | Clear tropical water over a sandy bottom, bright sunlight caustics, pale aqua gradient, open and empty |
