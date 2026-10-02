#!/usr/bin/env python3
"""Killion Remodeling — all client facts and page copy in one place.

Everything a human needs to change lives here. build.py turns it into HTML.

VOICE: the whole site is written in Rick's own first person — "I", "me", "my".
The only third-person copy is the demo chrome (banner, pop-up, footer note,
form notes), which is 60 Minute Sites speaking *about* Rick and must stay that
way. Those strings live in build.py and are marked DEMO.
"""

# ---------------------------------------------------------------- the business
# Spelling comes from the logo: REMODELING, one L. (An earlier logo file
# Rick sent spelled it with two; the current artwork is the one that counts.)
BIZ = "Killion Remodeling"
BIZ_SHORT = "Killion"
OWNER = "Rick"
OWNER_FULL = "Rick Killion"          # surname inferred from the business name

# Rick's real cell, given 2 Oct 2026. Written in the US format the rest of the
# site uses; he wrote it as 270.256.5483.
PHONE_DISPLAY = "(270) 256-5483"
PHONE_TEL = "2702565483"
PHONE_IS_PLACEHOLDER = False

EMAIL = "0507cubbies@gmail.com"       # real, from the call
CITY = "Bloomington"
STATE = "Illinois"
STATE_ABBR = "IL"
HOME_BASE = "Bloomington, Illinois"
RADIUS_MI = 50

# 60 Minute Sites plumbing
SIXTYMS_URL = "https://60minutesites.com"
PRICING_URL = "https://60minutesites.com/pricing.html"
FORM_ACTION = "https://60minutesites.com/form/general-contact-form-a935"

# ------------------------------------------------------------------- services
SERVICES = [
    dict(
        slug="handyman",
        name="Handyman & Home Repairs",
        short="Handyman & Repairs",
        kicker="The list you keep putting off",
        ico="wrench",
        blurb="One person for the whole honey-do list — the leaky sink, the door that sticks, "
              "the trim that rotted out, the shelf nobody ever hung.",
        hero_h="The List You Keep Putting Off",
        hero_p="Small jobs are most of what I do. Call me with one thing or ten — I would rather "
               "make one trip and knock out the lot.",
        lead="Most handyman calls start with one thing. A sink that drips. A door that will not "
             "latch. A board on the porch that gives a little when you step on it. By the time I "
             "am in the driveway there are usually four more, and that is fine — that is the job. "
             "Working through a list in one visit is cheaper for you than four separate trades on "
             "four separate days.",
        body=[
            ("Nothing is too small to call about",
             "Plenty of people sit on a repair for a year because it feels too minor to bother "
             "anyone with. Those are the calls I like. A dripping trap, a running toilet, a "
             "sticking storm door, a light switch that does nothing — half of them take me under "
             "an hour, and they are the ones that quietly drive you up the wall every single day."),
            ("How a visit usually goes",
             "Tell me what you have got over the phone and I will give you a feel for the time and "
             "the cost before I drive out. I turn up with the van loaded for general work, walk "
             "the list with you, and start at the top. If something turns out to be bigger than it "
             "looked — a soft subfloor under that loose tile, say — I stop and show you before I "
             "spend your money on it."),
        ],
        incl=[
            "Leaky faucets, traps, running toilets and shut-off valves",
            "Doors that stick, sag, will not latch or will not close",
            "Drywall patches, nail pops, water stains and texture touch-up",
            "Rotted trim, soffit, fascia and threshold replacement",
            "Loose railings, steps, gates and deck boards",
            "Shelving, closet systems, blinds, curtain rods and TV mounts",
            "Ceiling fans, light fixtures and switch and outlet swaps",
            "Caulking and sealing around tubs, sinks, windows and siding",
            "Furniture and fixture assembly, and the odd jobs nobody else will come out for",
        ],
        faqs=[
            ("Is there a minimum charge to come out?",
             "Ask me when you call. I will tell you straight what a short visit costs before I "
             "drive out, so there is no surprise at the end. For a list of several small jobs it "
             "almost always works out cheaper per item than booking them separately."),
            ("Will you look at a list, not just one job?",
             "That is how I would rather do it. Write down everything, including the things you "
             "think are too small to mention. I will work down the list and tell you if anything "
             "on it needs a licensed trade instead."),
            ("Do you do plumbing and electrical?",
             "The everyday repairs, yes — faucets, traps, toilets, valves, fixtures, fans, "
             "switches and outlets. Anything that means opening up a panel, moving a gas line or "
             "re-piping a house belongs with a licensed plumber or electrician, and I will say so "
             "rather than take a swing at it."),
            ("Can I text you a photo?",
             f"Yes, and it genuinely helps. Text me a picture on {PHONE_DISPLAY} and you will "
             "usually get a realistic answer on cost and timing without anyone having to drive "
             "anywhere."),
        ],
    ),
    dict(
        slug="painting",
        name="Interior & Exterior Painting",
        short="Painting",
        kicker="Clean lines, covered floors",
        ico="roller",
        blurb="Rooms, whole interiors, trim, ceilings, decks, siding and fences — prepped "
              "properly, cut in by hand, and cleaned up behind.",
        hero_h="Painting, Done Clean",
        hero_p="The paint is the easy part. The prep, the cut lines and leaving your house tidy "
               "are what you are actually paying for.",
        lead="Anyone can roll a wall. What separates a paint job that still looks right in five "
             "years from one that peels by next summer is everything that happens before the lid "
             "comes off — filling, sanding, caulking, priming the patches, and masking like I "
             "actually care about your carpet.",
        body=[
            ("Interior work",
             "Furniture moved to the middle and covered, floors run with drop cloths, and the "
             "room put back the same evening wherever I can. Holes filled and sanded flush, "
             "patches spot-primed so they do not flash through the topcoat, and trim and ceiling "
             "lines cut in by hand with a brush rather than taped and hoped for. One coat where "
             "one coat genuinely covers, two where it does not — and I will tell you which before "
             "I quote, not after."),
            ("Exterior work",
             "Siding washed down and left to dry, loose and flaking paint scraped back, bare wood "
             "primed, and gaps and end grain caulked so water has nowhere to sit. Then the colour. "
             "Decks, fences, soffit, fascia, shutters and front doors all fall under this too — a "
             "freshly painted front door and trim is the cheapest curb appeal anyone ever buys."),
        ],
        incl=[
            "Single rooms through to whole-house interiors",
            "Ceilings, walls, trim, doors, casing and baseboard",
            "Cabinet and built-in repainting",
            "Filling, sanding, caulking and spot-priming before any colour goes on",
            "Exterior siding, soffit, fascia, shutters and front doors",
            "Deck and fence staining, sealing and painting",
            "Water-stain and smoke-stain sealing before repaint",
            "Furniture moved and covered, floors protected, site cleaned down daily",
        ],
        faqs=[
            ("Do you supply the paint or do I?",
             "Either works. Most people have me pick it up so the right primer and the right sheen "
             "arrive with it, and the paint goes on your bill at cost. If you have already bought "
             "yours, or you are set on a particular brand, that is no problem at all."),
            ("How long does a room take?",
             "A straightforward bedroom with walls and ceiling is usually a day. Add trim, doors "
             "and a second coat and it stretches into a second day. Whole interiors get a schedule "
             "from me up front so you know which rooms are out of action on which days."),
            ("Can you match a colour I already have?",
             "Yes. Easiest is a chip off a hidden corner — inside a closet or behind a switch "
             "plate — which the paint counter can scan and match. If the original can is still in "
             "the basement, even better."),
            ("Is exterior painting worth it this time of year?",
             "It depends on the month and the forecast. Central Illinois gives a solid exterior "
             "season and I will tell you honestly if it is too cold, too wet or too late in the "
             "year for the paint to cure properly. A job that will fail by spring is not worth "
             "taking your money for."),
        ],
    ),
    dict(
        slug="decks-porches",
        name="Decks & Porches",
        short="Decks & Porches",
        kicker="Built, repaired, stained",
        ico="deck",
        blurb="New builds, board and railing replacement, wobbly steps made solid, and the "
              "stain and seal that keeps the whole thing from going grey.",
        hero_h="Decks & Porches",
        hero_p="A deck is the one part of a house that takes full Illinois weather with no roof "
               "over it. It needs looking after, and sometimes it needs rebuilding.",
        lead="Most deck calls I get are not for a whole new deck. They are for the three boards "
             "that have gone soft, the railing a guest leaned on and did not trust, and the four "
             "years of grey where the stain gave up. All of that is worth fixing — a sound frame "
             "with new decking and fresh stain costs a fraction of a tear-out.",
        body=[
            ("Repair before replacement",
             "I will tell you which one you need, and I will tell you the cheaper answer when the "
             "cheaper answer is the right one. Frames often outlast the boards on top of them by "
             "years. If the posts and joists are solid, swapping decking and railing gets you a "
             "deck that feels new for a lot less than a rebuild. If the structure has gone, I will "
             "say that too, and show you what I am looking at."),
            ("New builds and steps",
             "Ground-level decks, raised decks, landings and steps, railings and gates, and the "
             "little things that make a difference day to day — a gate that actually latches, "
             "steps that are the same height all the way up, a railing you can put your whole "
             "weight on. Stain or seal at the end, once the wood has had the time it needs to dry "
             "out enough to take it."),
        ],
        incl=[
            "New deck, landing and step construction",
            "Rotted board, joist and post replacement",
            "Railings, balusters, gates and handrails",
            "Loose, bouncy or uneven steps made solid",
            "Power washing, stripping and re-staining or sealing",
            "Pergolas, privacy screens and skirting",
            "Porch floor, column and ceiling repair",
            "Fence panel, post and gate repair while I am out there",
        ],
        faqs=[
            ("Can my deck be saved or does it need replacing?",
             "Usually saved. The frame underneath is often in much better shape than the walking "
             "surface, because the boards on top take the sun and the rain. I will get under "
             "there, check the posts and joists, and give you both prices so you can decide."),
            ("How soon after building can a new deck be stained?",
             "Treated lumber usually needs weeks to months of drying before it will take stain "
             "properly, depending on how wet it was when it arrived and what the weather does. "
             "Staining too early traps moisture and the finish fails. I will tell you roughly when "
             "to call me back for it."),
            ("Do you do railings on their own?",
             "Yes — that is a common call, often after someone has had a scare. New balusters, a "
             "new top rail, or posts reset and braced so the whole run stops moving."),
            ("What about the fence while you are here?",
             "Fence posts, panels and gates are the same sort of work and it is efficient to do "
             "them in the same visit. Mention it when you call so I bring the right materials."),
        ],
    ),
    dict(
        slug="windows-doors",
        name="Windows & Doors",
        short="Windows & Doors",
        kicker="Fitted square, sealed tight",
        ico="window",
        blurb="Replacement windows, exterior and interior doors, storm doors and screens — set "
              "level, sealed properly, and trimmed out to look like they belong.",
        hero_h="Windows & Doors",
        hero_p="A window or door is only as good as the fit. Set it out of square and no amount "
               "of weatherstripping saves it.",
        lead="Draughty windows and doors that have to be shouldered shut are two of the most "
             "common complaints in older central Illinois houses, and they are two of the most "
             "satisfying things I get to fix. The difference in a room is immediate — you can "
             "feel it standing next to the glass in January.",
        body=[
            ("Replacement windows",
             "Measured, ordered, fitted level and square, insulated and sealed around the frame, "
             "and trimmed out inside and out so the finish looks original rather than patched. One "
             "window because the seal has blown and it fogs up, or a run across the whole front of "
             "the house — both are the same job to me, just a different number of them."),
            ("Doors and storm doors",
             "Exterior doors hung so they close with a push rather than a shove, thresholds and "
             "sweeps that actually meet the door, deadbolts that line up with their strike, and "
             "rotted jamb and brickmould cut out and replaced instead of filled and painted over. "
             "Inside, I hang and case interior doors, bifolds and pocket doors. Storm doors and "
             "screens fitted or re-screened."),
        ],
        incl=[
            "Replacement window measuring, ordering and installation",
            "Blown or fogged sealed-unit replacement",
            "Exterior door and storm door installation",
            "Interior, closet, bifold and pocket doors hung and cased",
            "Rotted jamb, brickmould, sill and threshold replacement",
            "Weatherstripping, sweeps, thresholds and hardware",
            "Deadbolt, handle, strike plate and hinge repair and alignment",
            "Interior and exterior trim-out and painting to match",
        ],
        faqs=[
            ("Do you order the windows or should I?",
             "I will measure and order them, which matters more than it sounds — a replacement "
             "window measured off the old frame by eye is how you end up with a gap full of foam. "
             "If you have already bought windows, I will fit what you have."),
            ("My door closes but the draught is terrible. Replace it?",
             "Often not. A door that still shuts and latches can usually be fixed with new "
             "weatherstripping, a proper sweep, a threshold adjustment and the hinges and strike "
             "reset. Far cheaper than a new door, and it is worth trying first."),
            ("Can one fogged window be done on its own?",
             "Yes. A failed seal in one unit does not mean the rest need doing — it means that "
             "one unit failed. Replacing the glass alone is sometimes possible and is cheaper than "
             "the whole window."),
            ("Will the trim match the rest of the house?",
             "That is the aim and it is the part most people notice. I will match the existing "
             "profile as closely as what is available allows, and paint or stain it to blend in "
             "rather than leaving you a bright white frame in a room full of oak."),
        ],
    ),
    dict(
        slug="flooring",
        name="Tile & Carpet Flooring",
        short="Tile & Carpet",
        kicker="Flat floors, straight lines",
        ico="tile",
        blurb="Tile floors and backsplashes, carpet, and luxury vinyl plank — over a subfloor "
              "that has been checked first, which is where most bad floors go wrong.",
        hero_h="Tile & Carpet",
        hero_p="A floor is only as flat as what is underneath it. That is the part you never see "
               "and the part that decides whether the job lasts.",
        lead="Tile cracks and grout lines open up for one reason more than any other: movement "
             "underneath. Carpet ripples and seams show for much the same reason. So the first "
             "thing I do on a floor is pull a corner up and look at what I am tiling or laying "
             "over, before anybody talks about colours.",
        body=[
            ("Tile",
             "Floors, backsplashes, tub and shower surrounds, entryways and mud rooms. I check the "
             "subfloor and shore it up or level it first, put proper backer board or membrane "
             "where it belongs, set the layout out dry so the cuts land somewhere sensible rather "
             "than leaving a sliver at the doorway, then grout, seal and silicone where it needs "
             "to flex."),
            ("Carpet and vinyl plank",
             "Old flooring and tack strip pulled and hauled away, subfloor cleaned, squeaks "
             "screwed down while it is open, then new pad and carpet stretched in properly with "
             "seams put where the light does not catch them. Luxury vinyl plank is the one most "
             "people ask me about now and it earns the attention — it handles kitchens, basements, "
             "pets and kids better than almost anything at its price."),
        ],
        incl=[
            "Tile floors, entryways and mud rooms",
            "Kitchen backsplashes and tub and shower surrounds",
            "Subfloor repair, squeak fixing and levelling",
            "Backer board, membrane and waterproofing where it belongs",
            "Carpet and pad, stretched and seamed",
            "Luxury vinyl plank and sheet vinyl",
            "Transitions, thresholds, quarter-round and baseboard refit",
            "Old flooring tear-out and haul-away",
        ],
        faqs=[
            ("Can you tile over what is already there?",
             "Sometimes, and sometimes it is the wrong call. It depends what the existing surface "
             "is, how well it is stuck down and how much height you can afford to lose at the "
             "doors. I will look and tell you which, rather than tiling over a problem and handing "
             "it back to you in two years."),
            ("Who moves the furniture?",
             "I will, as part of the job. Just tell me what is fragile and what you would rather "
             "handle yourself, and clear the small stuff off surfaces before I arrive."),
            ("Tile or vinyl plank for a kitchen?",
             "Both are good. Tile is harder and cooler underfoot and lasts longest. Vinyl plank is "
             "warmer, quieter, much quicker to fit and a lot more forgiving if something gets "
             "dropped. I will give you my honest opinion for your room rather than the one with "
             "the bigger invoice."),
            ("Do you haul the old carpet away?",
             "Yes. Tear-out and disposal are part of my quote, so you are not left with a rolled "
             "carpet in the garage until next bulk-pickup day."),
        ],
    ),
    dict(
        slug="trim-carpentry",
        name="Trim & Finish Carpentry",
        short="Trim & Carpentry",
        kicker="The details people notice",
        ico="saw",
        blurb="Baseboard, casing, crown, chair rail, stair trim and built-ins — mitres that meet, "
              "caulked, filled and painted so nothing shows.",
        hero_h="Trim & Finish Carpentry",
        hero_p="Trim is the cheapest way to make an ordinary room look finished, and the easiest "
               "place to tell good work from rushed work.",
        lead="Finish carpentry is the last five percent of a room and about ninety percent of "
             "what a visitor actually notices. Gaps at the mitres, nail holes left proud, "
             "baseboard that waves along an uneven wall — all of it reads as sloppy even to "
             "people who could not tell you why.",
        body=[
            ("Trim work",
             "Baseboard, door and window casing, crown moulding, chair rail, wainscot and picture "
             "rail. I cut mitres to the wall rather than to the theory, scribe where a wall is "
             "out, glue and pin, then fill, caulk and sand before paint so the joints disappear "
             "instead of opening up over the first winter."),
            ("Built-ins and the rest",
             "Shelving, cubbies, bench seats, closet build-outs, mantels, stair skirt and tread "
             "trim, and the odd bit of custom work that is easier to build in place than to buy. "
             "If you have an awkward corner, an unused alcove or a landing that wastes space, that "
             "is usually a built-in waiting to happen."),
        ],
        incl=[
            "Baseboard, casing, crown, chair rail and wainscot",
            "Door and window trim-out after a replacement",
            "Stair skirt, tread, riser and newel trim",
            "Built-in shelving, benches, cubbies and closet build-outs",
            "Mantels, columns, beams and feature walls",
            "Rotted or damaged trim cut out and replaced in kind",
            "Filled, caulked, sanded and painted or stained to match",
            "Profile matching for older homes where the original is no longer sold",
        ],
        faqs=[
            ("Can you match the trim in my 1920s house?",
             "Usually close, and sometimes exactly. Plenty of older profiles are still made or can "
             "be built up from two or three stock pieces to sit right next to the original. Bring "
             "me a cut-off if you have one in the basement."),
            ("Is crown moulding a big job?",
             "Less than people expect in a square room, more than people expect in a room with "
             "bays, soffits or out-of-plumb corners. I will walk the room and give you a flat "
             "price rather than an hourly guess."),
            ("Do you paint the trim too?",
             "Yes, and it is usually best done as one job. Trim that is filled, caulked and "
             "painted by the same person who cut it tends to come out cleaner than trim that is "
             "handed over to somebody else a week later."),
            ("Can you build something custom?",
             "Within reason, and I will tell you when buying it would be cheaper than building "
             "it. Built-ins, benches and shelving that fit an awkward space are exactly where "
             "building beats buying."),
        ],
    ),
    dict(
        slug="room-additions",
        name="Room Additions & Bigger Projects",
        short="Room Additions",
        kicker="When the house needs more house",
        ico="house",
        blurb="Additions, basement finishing, garage and porch conversions and three-season "
              "rooms — planned properly, with a written quote and a start date.",
        hero_h="Room Additions & Bigger Projects",
        hero_p="The big ones need a plan, a permit and a real schedule. I will tell you what it "
               "takes before you commit to anything.",
        lead="Additions and finished basements are a different kind of job from a day of repairs, "
             "and they deserve a different kind of conversation. There is a drawing, a permit, an "
             "inspection schedule, trades to bring in at the right moment and a realistic start "
             "date. Anyone who gives you a firm number for this on the phone without seeing the "
             "house is guessing.",
        body=[
            ("What a bigger project looks like",
             "It starts with a walkthrough and a conversation about what you actually want the "
             "space to do. Then a written quote that itemises materials separately from labour, "
             "so you can see where the money goes and change your mind about a finish without the "
             "whole number moving. Then a start date I intend to keep, and one point of contact "
             "who is also the person swinging the hammer."),
            ("Where I bring in help",
             "I do the carpentry, the trim, the flooring and the painting myself. Structural "
             "engineering, significant electrical and plumbing, HVAC and anything that needs a "
             "licensed trade and a stamped inspection get the right licensed person, scheduled in "
             "at the right point so they are not tripping over each other. You will know who is "
             "coming and when."),
        ],
        incl=[
            "Room additions and bump-outs",
            "Basement finishing and egress work",
            "Garage, porch and attic conversions",
            "Three-season and sun rooms",
            "Framing, insulation, drywall and finish",
            "Flooring, trim and paint to tie the new space into the old",
            "Written itemised quote with materials and labour separated",
            "Licensed trades scheduled in for the parts that require them",
        ],
        faqs=[
            ("How accurate is the first number you give me?",
             "The first number over the phone is a range, and I will call it a range. The written "
             "quote after a walkthrough is the one to plan around. If something unexpected turns "
             "up once a wall is open, you hear about it from me that day with a price attached, "
             "before the work goes ahead."),
            ("Who deals with permits and inspections?",
             f"I pull the permits and schedule the inspections for the work I am doing. "
             f"Requirements differ between {CITY}, Normal and the smaller townships, and I will "
             "tell you what your particular job needs early rather than on the day."),
            ("Can I live in the house while you work?",
             "Nearly always, yes. I seal off the space I am working in and keep the dust out of "
             "the rest of the house as far as is realistic. I will be honest about the days that "
             "are genuinely disruptive — the demo, the concrete, the floor sanding — so you can "
             "plan around them."),
            ("Do you do full kitchen and bathroom remodels?",
             "No, and I would rather say so plainly than take the job and learn on your house. "
             "Full kitchens and bathrooms are their own specialism. I will happily do the parts "
             "that are mine — the tile, the flooring, the trim, the painting, the door — alongside "
             "whoever is handling the cabinets and the plumbing."),
        ],
    ),
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# -------------------------------------------------------------- service areas
# (town, miles from Bloomington, county) — all inside the 50-mile radius.
TOWNS = [
    ("Bloomington", 0, "McLean County"),
    ("Normal", 3, "McLean County"),
    ("Peoria", 42, "Peoria County"),
    ("Champaign", 50, "Champaign County"),
    ("Decatur", 48, "Macon County"),
    ("Pontiac", 36, "Livingston County"),
    ("Lincoln", 34, "Logan County"),
    ("Morton", 38, "Tazewell County"),
    ("Washington", 41, "Tazewell County"),
    ("Clinton", 24, "DeWitt County"),
    ("Mahomet", 40, "Champaign County"),
    ("Eureka", 30, "Woodford County"),
    ("El Paso", 25, "Woodford County"),
    ("Le Roy", 18, "McLean County"),
    ("Heyworth", 14, "McLean County"),
    ("Hudson", 11, "McLean County"),
    ("Towanda", 9, "McLean County"),
    ("Lexington", 17, "McLean County"),
    ("Chenoa", 23, "McLean County"),
    ("Downs", 11, "McLean County"),
    ("Carlock", 15, "McLean County"),
    ("Danvers", 15, "McLean County"),
    ("Farmer City", 26, "DeWitt County"),
    ("Fairbury", 33, "Livingston County"),
]

# Pins on the CSS radius map: (town, left %, top %) — eyeballed, not surveyed.
MAP_PINS = [
    ("Peoria", 17, 34),
    ("Pontiac", 73, 18),
    ("Champaign", 84, 70),
    ("Decatur", 30, 84),
    ("Lincoln", 22, 70),
    ("Clinton", 38, 69),
    ("El Paso", 40, 26),
    ("Le Roy", 63, 60),
    ("Fairbury", 76, 32),
    ("Eureka", 28, 38),
]

# --------------------------------------------------------------- how it works
STEPS = [
    ("Tell me what you have got",
     "Call, text or send the form. Photos help more than descriptions — text them straight to my "
     "phone. I answer my own calls, so you are not going through an office."),
    ("I come and look, free",
     "For anything beyond a small repair I will come out, walk it with you and measure up. There "
     "is no charge for the estimate and no sales pitch at the end of it."),
    ("You get a straight number",
     "Small jobs get a price on the spot. Bigger ones get it in writing with the materials "
     "itemised separately, so you can see what you are paying for."),
    ("I do the work myself",
     "I am the one who shows up. No crew you have never met, no subcontractor you were not told "
     "about. Floors covered, mess cleaned up, and I do not leave a job half finished to go start "
     "another one."),
]

# ------------------------------------------------------------------ why me
WHY = [
    ("You get me, start to finish",
     "You deal with me from the first phone call to the last bit of clean-up. Nobody hands you "
     "off, nobody turns up who you have not met, and nobody tells you they will have to check "
     "with the office."),
    ("One person for a list of jobs",
     "Most houses do not need a specialist. They need somebody competent who can paint the "
     "bedroom, fix the sink, re-hang the door and sort the deck boards without you coordinating "
     "four separate trades."),
    ("I will tell you when not to spend money",
     "If the cheaper repair is the right answer, that is what you will hear from me. If a job "
     "needs a licensed plumber or electrician, I will say so instead of taking a run at it."),
    ("Free estimates and straight answers",
     "No charge for me to come and look at anything substantial, no pressure at the end, and a "
     "real number rather than a range that quietly doubles once work starts."),
]

# -------------------------------------------------------------- how pricing works
# Deliberately no dollar figures — Rick has not given any. This explains the
# shape of his pricing instead, which is what people actually want to know.
PRICING_ROWS = [
    ("A few small repairs, one visit", "Hourly, quoted before I drive out"),
    ("A room or two to paint", "Flat price after a quick walkthrough"),
    ("Deck, windows, flooring, trim", "Written quote, materials listed separately"),
    ("Additions and bigger builds", "Written itemised quote with a start date"),
]

# --------------------------------------------------------------- general FAQs
GENERAL_FAQS = [
    ("What exactly do you do?",
     "Handyman work and painting, mostly, plus the trades that sit around them — decks and "
     "porches, windows and doors, tile and carpet, trim and finish carpentry, and room additions "
     "when somebody needs more house. If it is a repair, a refresh or a small build, it is "
     "probably on my list."),
    ("What do you not do?",
     "Full kitchen and bathroom remodels. I will do the tile, the flooring, the trim, the "
     "painting and the doors in a kitchen or bathroom, but the whole gut-and-rebuild belongs with "
     "somebody who does nothing else. I would rather tell you that than learn on your house."),
    ("How far do you travel?",
     f"About {RADIUS_MI} miles around {HOME_BASE} — that covers {CITY} and Normal out to Peoria, "
     "Champaign, Decatur, Pontiac and Lincoln, and all the smaller towns in between. If you are "
     "just outside it, call me anyway and ask."),
    ("Are you new? I have not heard of you.",
     f"Not new to the work, but new again to {CITY}. I was busy here a few years back, was away "
     "for a stretch, and I am building the customer list back up. That is the honest reason you "
     "have not seen my truck on your street yet — and the reason I am as keen as I am to do a "
     "good job for the first people who call."),
    ("Do you charge for an estimate?",
     "No. Anything beyond a quick small repair gets a free visit, a look and a number. Small "
     "repairs get a price over the phone so neither of us wastes a trip."),
    ("How quickly can you start?",
     "Small jobs are often the same week. Bigger ones get a real start date rather than a vague "
     "promise. Call and ask me what the next couple of weeks look like — the answer changes."),
    ("Can I just text you?",
     f"Yes, and most people do. Text {PHONE_DISPLAY} with a photo and a sentence about what you "
     "need and you will get a straight answer back."),
]

# -------------------------------------------------------------------- photos
# Library photographs standing in until Rick sends his own. Sources and
# licence are on credits.html and in DEMO-NOTES.md.
#   key: (file, alt text)
PHOTOS = {
    "hero":              ("hero.jpg", "A painter on a ladder working along the upper siding of a grey house against a blue sky"),
    "rick-at-work":      ("rick-at-work.jpg", "A tradesman in a tool belt reaching into an open tool case on a job"),
    "painting-interior": ("painting-interior.jpg", "Two people rolling fresh paint onto the walls of a bright empty room"),
    "painting-detail":   ("painting-detail.jpg", "A hand cutting in a door frame with a paint brush"),
    "painting-exterior": ("painting-exterior.jpg", "A painter working between two ladders on the wooden siding of a house"),
    "painted-room":      ("painted-room.jpg", "A freshly painted room with white walls, exposed beams and a wood floor"),
    "handyman-repair":   ("handyman-repair.jpg", "An old window being repaired, with a hammer and drill resting on the sill"),
    "tools":             ("tools.jpg", "Hand tools laid out on a workbench"),
    "deck-finished":     ("deck-finished.jpg", "A finished raised deck with black railings on the back of a brick house"),
    "deck-repair":       ("deck-repair.jpg", "A hammer driving a nail into a deck board"),
    "deck-build":        ("deck-build.jpg", "A tape measure held across a length of fresh timber"),
    "window-install":    ("window-install.jpg", "A new window set into an opening, still part-wrapped in protective film"),
    "window-work":       ("window-work.jpg", "A fitter in a cap working on the frame of a large window"),
    "door-exterior":     ("door-exterior.jpg", "A grey house with white porch columns, white trim and a wooden front door"),
    "flooring-plank":    ("flooring-plank.jpg", "Hands laying a plank of dark wood flooring into place"),
    "carpet-room":       ("carpet-room.jpg", "An empty room with new carpet and freshly painted white walls"),
    "tile-detail":       ("tile-detail.jpg", "A brass valve set into a wall of white subway tile"),
    "trim-work":         ("trim-work.jpg", "A carpenter kneeling to drill into a door casing"),
    "trim-saw":          ("trim-saw.jpg", "A mitre saw surrounded by offcuts of trim"),
    "carpentry-mark":    ("carpentry-mark.jpg", "Hands marking a cut line on a board with a pencil"),
    "living-room":       ("living-room.jpg", "A finished living room with a wood stove, pale walls and large windows"),
    "room-bright":       ("room-bright.jpg", "A bright living room with a fireplace and tall windows either side"),
}

# the gallery, in display order
GALLERY = [
    "rick-at-work", "painting-interior", "painted-room", "deck-finished",
    "handyman-repair", "window-install", "flooring-plank", "trim-work",
    "painting-exterior", "carpet-room", "tile-detail", "deck-repair",
    "painting-detail", "door-exterior", "trim-saw", "living-room",
    "carpentry-mark", "window-work", "room-bright", "deck-build", "tools",
]

# main photo + supporting photos per service page
SERVICE_PHOTOS = {
    "handyman":       ("handyman-repair", ["tools", "rick-at-work"]),
    "painting":       ("painting-interior", ["painting-detail", "painted-room", "painting-exterior"]),
    "decks-porches":  ("deck-finished", ["deck-repair", "deck-build"]),
    "windows-doors":  ("window-install", ["window-work", "door-exterior"]),
    "flooring":       ("flooring-plank", ["tile-detail", "carpet-room"]),
    "trim-carpentry": ("trim-work", ["trim-saw", "carpentry-mark"]),
    "room-additions": ("living-room", ["room-bright", "carpentry-mark"]),
}

# card image per service, for the grids
SERVICE_CARD_PHOTO = {
    "handyman": "handyman-repair",
    "painting": "painting-interior",
    "decks-porches": "deck-finished",
    "windows-doors": "window-install",
    "flooring": "flooring-plank",
    "trim-carpentry": "trim-work",
    "room-additions": "living-room",
}
