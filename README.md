# osuAvatarImport
Very simple tool to import avatars for use in tournaments.

## How does it work?
The script gets user list from usernames.csv file, then if usernames are provided it requests user ids from bancho (for which you **NEED** api key, which you can get [here](https://osu.ppy.sh/p/api/)), you will get asked for one on first run. After this it will download avatars to /avatars folder.
### Avatar file naming scheme.
Every character is lowercase with special ones changed to underscore (_).
## Help. The program doesn't work!
Well, make sure you have correct api key added in config.cfg. Afterwards you can check if the user even has avatar (default one isn't downloaded for now, I'm fairly certain restricted users' aren't available too). If this doesn't work, create issue on github explaining the issue **WITH** *logs.log* file included.
