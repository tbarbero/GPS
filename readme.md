# Introduction

This repository includes the code that will automate data transfer from a GPS
to a server.

### What are we doing?

The Evan Research Lab aims to study how the shrinking Salton Sea will
influence dust storm activity in the region surrounding it. We constructed a
research site that will provide us with continuous data of aerosols, boundary
layer structure, water vapor, and radiative fluxes.

### My role

I utilize a Trimble NetR9 GNSS Receiver. It communicates with satellites and
records observables, one of which is the pseuorange. The pseudorange is the 
absolute path the signal travels from GPS satellite to receiver on the ground.
We're able to isolate the length of the path caused by water vapor. With a 
technique called retrieval, we will be able to estimate the water vapor
in the atmosphere. Here, I write the code that will automate data transfer
from the GPS receiver to our server.
