"""
Scriptwriter Agent for History of Earth (Cinematic YouTube Screenplay Engine).
Produces high-retention, 7-scene episodic movie screenplays with dramatic hooks,
continuous pacing, and a high-stakes mysterious cliffhanger ending.
"""

from typing import Dict, List, Any, Optional

CINEMATIC_SCENES = [
    {
        "scene_id": 1,
        "title": "THE DEATH OF A SISTER WORLD",
        "scene_type": "theia_impact",
        "scene_asset": "assets/scenes/theia_impact.jpg",
        "camera_style": "rapid_impact_zoom_with_shake",
        "narration": (
            "Look at the ground beneath your feet. It feels solid. Permanent. Safe.\n\n"
            "Four and a half billion years ago, there was no ground. There was only fire, poison, and a sky that wanted to kill you.\n\n"
            "In the blackness of the newborn solar system, a rogue planet named Theia—the size of Mars—is screaming through the dark at twenty-five thousand miles per hour. "
            "It is locked on a direct collision course with the infant Earth.\n\n"
            "The impact does not merely crack the crust. It obliterates it. Trillions of tons of vaporized mantle detonate into space, lighting up the void with a blinding kinetic supernova."
        )
    },
    {
        "scene_id": 2,
        "title": "A WORLD OF LIQUID ROCK",
        "scene_type": "magma_ocean",
        "scene_asset": "assets/scenes/magma_ocean.jpg",
        "camera_style": "panoramic_lava_tracking_sweep",
        "narration": (
            "From the ashes of that planetary collision rises a nightmare: an unbroken ocean of boiling magma, one thousand kilometers deep.\n\n"
            "Tides of liquid basalt surge across the burning horizon, pulled by a newborn Moon orbiting terrifyingly close—dominating half the blood-red sky.\n\n"
            "For tens of millions of years, the inferno refuses to sleep. Heavy molten iron plunges through liquid rock toward the center, forging the planet’s magnetic shield. "
            "Earth is hammering out its heart inside a planetary furnace."
        )
    },
    {
        "scene_id": 3,
        "title": "THE GREAT CONDENSATION",
        "scene_type": "torrential_rain",
        "scene_asset": "assets/scenes/torrential_rain.jpg",
        "camera_style": "vertical_lightning_deluge_tilt",
        "narration": (
            "Above the magma waves, the atmosphere is a crushing vault of supercritical steam and sulfur, with pressure fierce enough to pulverize steel.\n\n"
            "Then, temperature physics hits an irreversible tipping point. The planet drops below three hundred degrees Celsius... and the sky shatters.\n\n"
            "Rain falls continuously for centuries. Torrential, boiling, acidic downpours crash onto cooling basalt rocks. "
            "Steam geysers roar into the emerald clouds, only to fall again, pooling into Earth’s very first ocean: scalding, emerald-green, and saturated with dissolved iron."
        )
    },
    {
        "scene_id": 4,
        "title": "THE IMPOSSIBLE WITNESS",
        "scene_type": "jack_hills_zircon",
        "scene_asset": "assets/scenes/jack_hills_zircon.jpg",
        "camera_style": "macro_luminescence_dolly",
        "narration": (
            "For decades, science taught that the Hadean was an unlivable wasteland—a hell with no memory.\n\n"
            "They were wrong.\n\n"
            "In the ancient red dirt of Western Australia's Jack Hills, geologists extracted a microscopic crystal no thicker than a human hair: a zircon grain, dated to 4.404 billion years old.\n\n"
            "Trapped inside its atomic lattice was an impossible secret: oxygen isotope signatures proving that cool liquid water and granitic continents existed almost immediately after the magma sea froze."
        )
    },
    {
        "scene_id": 5,
        "title": "THE FINAL BOMBARDMENT",
        "scene_type": "late_bombardment",
        "scene_asset": "assets/scenes/late_bombardment.jpg",
        "camera_style": "crane_pullback_meteor_shockwaves",
        "narration": (
            "Yet just as the crust began to heal, the universe launched a final, cataclysmic assault: the Late Heavy Bombardment.\n\n"
            "Asteroids the size of entire mountain ranges rained down from the sky, detonating like thermonuclear warheads across the boiling oceans.\n\n"
            "Yet against all astronomical odds, Earth held. Every drop of water in your cells, every mineral in your bones, and the ground beneath your feet was forged in this dawn of fire."
        )
    },
    {
        "scene_id": 6,
        "title": "INTO THE BLACK ABYSS",
        "scene_type": "hydrothermal_vent",
        "scene_asset": "assets/scenes/hydrothermal_vent.jpg",
        "camera_style": "deep_abyssal_descent",
        "narration": (
            "The firestorms above eventually faded. But the real story wasn't happening on the surface.\n\n"
            "Four miles beneath the boiling green waves, in total and suffocating blackness, the sea floor opened up.\n\n"
            "Towering mineral chimneys—black smokers—began spewing superheated chemical soups into the dark. Heat, pressure, and volcanic sulfur met for the first time in an abyssal cauldron."
        )
    },
    {
        "scene_id": 7,
        "title": "THE MYSTERIOUS AWAKENING (CLIFFHANGER)",
        "scene_type": "life_spark_cliffhanger",
        "scene_asset": "assets/scenes/life_spark_cliffhanger.jpg",
        "camera_style": "mysterious_macro_spark_drift",
        "narration": (
            "And here, in the pitch-black depths of this volcanic grave... something impossible began to stir.\n\n"
            "Microscopic organic molecules were locking together on metallic crystals, forming the first self-replicating chains.\n\n"
            "Chemistry was crossing the forbidden threshold into code. Dead rock was learning to breathe.\n\n"
            "How did poisonous chemical dust spark into life? And what looming planetary catastrophe almost snuffed it out before it could even begin?\n\n"
            "Next time, on History of Earth: The Archean Dawn — The Secret of the Black Smokers.\n\n"
            "Hit subscribe, and ring the bell. Because Earth's darkest mystery... has only just begun."
        )
    }
]


CINEMATIC_SCENES_HADEAN_MAP = [
    {
        "scene_id": 1,
        "title": "THE UNBROKEN PRISON",
        "scene_type": "stagnant_lid_sphere",
        "scene_asset": "pipeline/cinematic_animator.py:1",
        "camera_style": "3d_orbital_scan_with_detective_hud",
        "mood": "cosmic_mystery",
        "narration": (
            "Open any geology textbook in the world, and you will find a map of plates. "
            "Fifteen colossal jigsaw pieces sliding, colliding, and recycling the surface of the Earth.\n\n"
            "Continental drift is the master engine of our world. But rewind the clock four point four billion years... and that engine did not exist.\n\n"
            "In the dawn of the Hadean eon, our planet was trapped in a single, unbroken rocky cage. "
            "No Pacific plate. No Atlantic rift. No subduction trenches. Just one monolithic, rigid basalt shell capping a churning planetary mantle.\n\n"
            "Geophysicists call this the Stagnant Lid. And for five hundred million years, Earth was a world with no plates."
        )
    },
    {
        "scene_id": 2,
        "title": "THE HEAT-PIPE FURNACE",
        "scene_type": "heat_pipe_furnace",
        "scene_asset": "pipeline/cinematic_animator.py:2",
        "camera_style": "mantle_cross_section_convection_loops",
        "mood": "internal_furnace",
        "narration": (
            "Underneath this unbroken crust, a monstrous engine was trapped.\n\n"
            "Primordial radioactivity was three times hotter than today. "
            "Billions of tons of molten rock churned violently against the ceiling of the shell with nowhere to go.\n\n"
            "Without plate tectonics to pull cool crust down, how did Earth keep from detonating?\n\n"
            "It survived through an alien mechanism: volcanic heat pipes. "
            "Towering conduits pierced straight through the shell, pumping torrential flood basalts across the surface—cooling the interior through continuous, apocalyptic eruption. "
            "Earth did not drift. It boiled in place."
        )
    },
    {
        "scene_id": 3,
        "title": "THE 500-MILLION-YEAR CRIME SCENE",
        "scene_type": "vanished_world_timeline",
        "scene_asset": "pipeline/cinematic_animator.py:3",
        "camera_style": "geological_column_laser_disintegration",
        "mood": "forensic_investigation",
        "narration": (
            "Here is the detective mystery that kept geologists awake for a century.\n\n"
            "If Earth was locked in a stagnant lid... where did all the evidence go?\n\n"
            "Every square mile of modern oceanic crust is recycled within two hundred million years. "
            "And of the ancient Hadean rock that formed this planetary shell? Exactly zero percent survives intact. Not a single cliff. Not a single boulder.\n\n"
            "Five hundred million years of planetary history... erased from the geologic record.\n\n"
            "How do we know the stagnant lid existed? And what clues could possibly survive a half-billion-year forensic void?"
        )
    },
    {
        "scene_id": 4,
        "title": "THE ATOMIC WITNESS",
        "scene_type": "zircon_mass_spectrometry",
        "scene_asset": "pipeline/cinematic_animator.py:4",
        "camera_style": "laser_ablation_mass_spectrometry",
        "mood": "atomic_discovery",
        "narration": (
            "The answer was hiding inside a microscopic time capsule.\n\n"
            "In the ancient red dirt of Western Australia's Jack Hills, scientists discovered tiny, indestructible mineral crystals: detrital zircons, dated to 4.404 billion years ago.\n\n"
            "When geochemists fired secondary ion mass spectrometers and atom-probe tomography beams into their crystal lattice, they uncovered an impossible chemical signature.\n\n"
            "The titanium-in-zircon thermometer revealed crystallization temperatures of just six hundred and eighty degrees Celsius.\n\n"
            "Dry basalt under a stagnant lid melts at eleven hundred degrees. "
            "Six hundred and eighty degrees can only mean one thing: granite forming in the presence of water. The stagnant shell had an invisible fracture."
        )
    },
    {
        "scene_id": 5,
        "title": "THE GREAT RUPTURE",
        "scene_type": "great_rupture_subduction",
        "scene_asset": "pipeline/cinematic_animator.py:5",
        "camera_style": "lithospheric_fracture_subduction_descent",
        "mood": "tectonic_rupture",
        "narration": (
            "Over hundreds of millions of years, the cold basalt shell grew thicker and heavier, until gravitational instability reached a catastrophic tipping point.\n\n"
            "The rigid shell began to buckle under its own immense weight.\n\n"
            "Then, across thousands of miles of primordial ocean... the lid cracked.\n\n"
            "Cold, dense oceanic crust broke free and plunged downward into the incandescent mantle. The very first subduction zone on Earth was born.\n\n"
            "Frictional shear heating lit up the fault plane with blinding energy, unleashing planet-shattering megaquakes as mobile plate tectonics awakened for the very first time."
        )
    },
    {
        "scene_id": 6,
        "title": "FORGING THE ANCESTORS",
        "scene_type": "birth_of_cratons",
        "scene_asset": "pipeline/cinematic_animator.py:6",
        "camera_style": "island_arc_collision_cratonic_keel",
        "mood": "continental_majesty",
        "narration": (
            "As the hydrated oceanic slab plunged into the mantle, it triggered a miracle of chemistry.\n\n"
            "Water lowered the melting point of rock, creating buoyant, silica-rich granitic magmas that bubbled toward the surface.\n\n"
            "Volcanic island arcs drifted together on conveyor belts of rock, crashing and fusing into the first stable, buoyant landmasses: cratons.\n\n"
            "The Pilbara Craton in Australia. The Kaapvaal Craton in Africa. Light enough to float on the mantle, and strong enough to endure four billion years of planetary violence.\n\n"
            "These were not just rocks. They were the ancient great-grandfathers of Pangaea—and the bedrock of the continents we walk on today."
        )
    },
    {
        "scene_id": 7,
        "title": "THE DEGASSING INFERNO (CLIFFHANGER)",
        "scene_type": "degassing_crisis_cliffhanger",
        "scene_asset": "pipeline/cinematic_animator.py:7",
        "camera_style": "supervolcanic_outgassing_greenhouse_surge",
        "mood": "cliffhanger_suspense",
        "narration": (
            "The birth of moving plates saved Earth from a dead stagnant fate. But it ignited a brand new planetary catastrophe.\n\n"
            "As billions of tons of water-soaked crust plunged into the deep mantle, the planet exhaled.\n\n"
            "Monstrous volcanic arcs exploded across the globe, pumping gigatons of steam, carbon dioxide, and poisonous sulfur into the sky.\n\n"
            "Atmospheric pressure soared to nearly one hundred atmospheres. The skies choked into a suffocating, boiling green vault of acid and darkness.\n\n"
            "How did Earth survive a runaway greenhouse inferno? And what triggered the deluge of boiling rain that forged the world's first ocean?\n\n"
            "Next time, on History of Earth: The Sky Was Poison and the Rain Never Stopped.\n\n"
            "Subscribe, ring the bell, and join us... as the clouds begin to fall."
        )
    }
]


def write_script(
    approved_claims: List[Dict[str, Any]],
    variation_constraints: Optional[Dict[str, Any]] = None,
    pillar: str = "Map"
) -> Dict[str, Any]:
    """
    Assembles the 7-scene cinematic movie screenplay with high-retention pacing,
    theatrical acting cues, and the mysterious cliffhanger ending.
    """
    if pillar.lower() == "map":
        scenes = CINEMATIC_SCENES_HADEAN_MAP
        next_hook = "The Sky Was Poison and the Rain Never Stopped"
    else:
        scenes = CINEMATIC_SCENES
        next_hook = "The Archean Dawn: The Secret of the Black Smokers"

    shot_list = []
    full_script_blocks = []
    current_time_sec = 0.0

    for scene in scenes:
        scene_text = scene["narration"].strip()
        full_script_blocks.append(f"=== SCENE {scene['scene_id']}: {scene['title']} ===\n{scene_text}")

        # Dramatic trailer cadence: ~2.1 words/sec
        words = len(scene_text.split())
        dur = max(20, int(words / 2.1))

        m_start, s_start = divmod(int(current_time_sec), 60)
        current_time_sec += dur
        m_end, s_end = divmod(int(current_time_sec), 60)

        shot_list.append({
            "shot_id": scene["scene_id"],
            "scene_title": scene["title"],
            "scene_type": scene["scene_type"],
            "scene_asset": scene["scene_asset"],
            "camera_move": scene["camera_style"],
            "mood": scene.get("mood", "cosmic_mystery"),
            "narration_segment": scene_text,
            "duration_sec": dur,
            "timestamp_start": f"{m_start:02d}:{s_start:02d}",
            "timestamp_end": f"{m_end:02d}:{s_end:02d}"
        })

    full_script_text = "\n\n".join(full_script_blocks)

    return {
        "script_text": full_script_text,
        "shot_list": shot_list,
        "runtime_estimate_sec": int(current_time_sec),
        "metadata": {
            "total_scenes": len(scenes),
            "cliffhanger_present": True,
            "next_episode_hook": next_hook,
            "word_count": len(full_script_text.split())
        }
    }


if __name__ == "__main__":
    res = write_script([])
    print(f"Generated 7-Scene Screenplay ({res['runtime_estimate_sec']}s):")
    for s in res["shot_list"]:
        print(f"  [{s['timestamp_start']} - {s['timestamp_end']}] {s['scene_title']}")
