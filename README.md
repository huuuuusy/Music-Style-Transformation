# INTRODUCTION

In this project, we want to construct a music style converter that can use machine learning algorithms to perform style conversions for the input  MIDI music.  We chose jazz music as a goal of conversion. The overall thinking is as follows:

First, select 800 jazz to build the original data set, and divide the data set into three parts: 

|Folder|Songs|
|:--:|:--:|
|train|600|
|dev|50|
|test|150|

Then, use music21 to extract information from the original MIDI song and retrieve its track information to save in the txt file.

Next, for the track information in each txt file, split it and get the chord and note sperately, save these two information in different files. This step is done for all folders. 

Finally we get six files: 

train.chord, train.note, dev.chord, dev.note, test.chord, test.note.

After that, we will use Tensorflow NMT to accomplish the training process. We regard the chord file as the source sequence while the note file as the target sequence. Based on this, the NMT will be trained to accomplish the chord to note transfermation. Since the target notes are collected from jazz songs, if we input a new song's chord file, the NMT will search the corresponding　jazz note to combine the jazz-style note file. Thus, by using the input song and the jazz-style note file, we can generate a new song with jazz style based on music21's functions.
