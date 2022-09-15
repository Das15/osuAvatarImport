# osuAvatarImport
Very simple tool to import avatars for use in tournaments.

## How does it work?
It gets user list from usernames.csv file, then if usernames are provided it requests user ids from bancho (for which you **NEED** api key, which you can get [here](https://osu.ppy.sh/p/api/). After this it will download avatars to /avatars folder.
### Avatar file naming scheme
Every character is lowercase with special ones changed to underscore (_).
