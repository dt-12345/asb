# ASB

This is a WIP so old ASB JSON versions may not work with updates, if you're having issues, make sure you have the latest version of both the JSONs and the scripts

A few notes:

- Animation events present in ASB appear to be fake and all events are actually controlled by BAEV files
- If you create a custom ASB file that requires animation events, remember to have a corresponding BAEV file with the same name

You'll have to run this with Python yourself for now, use `asb_to_json` or `json_to_asb` with the proper arguments like so:

```py
import asb

asb.asb_to_json("Lynel.root.asb")
```

Sorry for the lack of command line support, but hopefully this is not too hard to figure out :P