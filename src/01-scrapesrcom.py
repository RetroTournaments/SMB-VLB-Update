# This script is the first script.
# It uses srcomapi (https://github.com/blha303/srcomapi) to scrape speedrun.com and identify all of the runs that must be recreated
# To install srcomapi follow the directions at the above link.

# This creates (with some user interaction..) a csv (01-runs.csv) that lists all of the runs and relevant information for the next step.

import srcomapi
import srcomapi.datatypes as dt

TIME_CUTOFF_MS = 300000
OUTPUT = "01-runs.csv"

api = srcomapi.SpeedrunCom()
smb = api.search(srcomapi.datatypes.Game, {"name": "super mario bros."})[0]
anyp = smb.categories[0]

lb = dt.Leaderboard(api, 
        data=api.get("leaderboards/{}/category/{}?embed=variables".format(smb.id, anyp.id)))

lines = []
seen = set()

with open(OUTPUT, "r") as f:
    f.readline()
    for line in f.readlines():
        lines.append(line)
        seen.add(line.split(",")[0])



with open (OUTPUT, "w") as f:
    f.write("src_run_id,src_platform_id,src_region_id,display_name,date_played,elapsed_ms,video_url\n")
    for line in lines:
        f.write(line)

    for r in lb.runs:
        srcrun = r["run"]
        src_run_id = srcrun.id
        elapsed_ms = srcrun.times["primary_t"] * 1000

        if src_run_id in seen:
            continue

        if elapsed_ms > TIME_CUTOFF_MS:
            continue

        src_platform_id = srcrun.system["platform"]
        src_region_id = srcrun.system["region"]
        if src_region_id is None:
            src_region_id = "pr184lqn" # this is a hold-over from 2021 that I don't remember why.


        display_name = srcrun.players[0].name
        date_played = srcrun.date

        url = None
        if srcrun.videos is not None:
            if "links" in srcrun.videos:
                urls = []
                for l in srcrun.videos["links"]:
                    urls.append(l["uri"])

                if len(urls) == 1:
                    url = urls[0]
                else:
                    print(f"CHOOSE BEST VIDEO: www.speedrun.com/smb1/run/{src_run_id}")
                    for i, turl in enumerate(urls):
                        print(i, turl)

                    l = input("index: ")
                    url = urls[int(l)]

        if url is not None:
            while url.find('&') != -1:
                print(url)
                print("WARNING URL CONTAINS AN '&', enter updated url")
                url = input("url: ")


        print(f"{src_run_id},{src_platform_id},{src_region_id},{display_name},{date_played},{elapsed_ms},{url}\n")
        f.write(f"{src_run_id},{src_platform_id},{src_region_id},{display_name},{date_played},{elapsed_ms},{url}\n")

