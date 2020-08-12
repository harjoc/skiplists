# skiplists
This is a collection of skip lists that remove scenes with smoking, illegal drugs and sex from movies. Playable in VLC.

An XSPF file contains a list of scenes that should be skipped. To play it, you also need the actual AVI/MP4/etc video file. Place the XSPF in the same directory as the video file, and rename your video file to match the XSPF filename. And that's it. You can open the XSPF in VLC, and play it.

The `.xspf` files are generated using `skiplist.py` from `.skip` files, which have the same format as `.srt` files, and can be created using a subtitle editor.
