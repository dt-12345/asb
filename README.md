# ASB

Some scripts to work with ASB and BAEV files

You'll have to run this with Python yourself for now, use `asb_to_json` or `json_to_asb` with the proper arguments like so:

```py
import converter

# optional output_dir argument specifies the output location for the file
# optional romfs_path argument specifies the romfs location for zs compression/decompression
# optional compress_file argument specifies whether or not to compress the file with zstd

# optional baev_path argument loads the corresponding BAEV file with the ASB
converter.asb_to_json("Lynel.root.asb", "output_folder", baev_path="Lynel.root.baev")

converter.json_to_asb("Lynel.root.json", "output_folder")

converter.baev_to_json("Enemy_Lynel_Animation.anim.baev")

converter.json_to_baev("Enemy_Lynel_Animation.anim.baev", compress_file=True)
```

Sorry for the lack of command line support, but hopefully this is not too hard to figure out :P

It will automatically store your romfs path in `romfs.txt` after the first time you run it so you shouldn't have to provide it again afterwards.

May take a second or two to run for larger files, it's not the fastest

BAEV files control the animation events - events inside the ASB file do not do anything (at least in TotK, games that do not support BAEV files may use the ASB events instead).

There are two types of BAEV files: Animation and AsNode BAEV files. Animation BAEV files are linked to `.anim.bfres` files and the hashes inside are hashes of the corresponding animation name. AsNode BAEV files are linked to `.asb` files and the hashes inside are the hashes of the corresponding event node's GUID. When loading a BAEV file with an ASB file, make sure it is the correct one or nothing will happen.

The BAEV file must be named the same as its `.asb`/`.anim.bfres` file in order for the game to find it.