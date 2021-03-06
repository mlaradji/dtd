# dtd: Double Triangle Descendants
This is a project aimed at producing efficient code for handling and enumerating double-triangle descendants, with a focus on 4-regular graphs and especially K_5-descendants.

# Getting Started
Check out the two `.ipynb` files in the examples folder.

As of now, only DTEGraph and eGraph are explained. Other modules might be useable, and have detailed help text. A proper tutorial for them is planned.

# Requirements

SageMath 8 is perhaps the only requirement. An `ipynb` reader is required to read the examples.

# Features

eGraph - Contains eGraph, a general extension of the sage Graph object, DTEGraph, an extension of eGraph with double triangle operations, and PDGraph, an extension of DTEGraph for pseudodescendants such as K_5-descendants. PDGraph is buggy and is being improved.

eGraphSet - Contains eGraphSet, which is a general indexed set that has additional functions to deal with graph members, and Family and K5Family which contain functions specific to double triangle families.

parts - Contains objects that make up pseudodescendants, such as Zigzag's and Chain's. It is currently quite buggy, but feedback is welcome.
