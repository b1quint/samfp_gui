#!/bin/csh -f

# General parameters:
#      - You requested to use the following FP: Thickness = 200 microns; tunable gap = 2 microns; p=609 @ Halpha 
#      - You requested to do a OBSERVATION (and not a calibration)
#      - The name of the object                         : RR01_J1741
#      - The wavelength (at rest) you gave is             = 6562.78 angstroms
#      - The radial velocity is                           = 0 km/s
#      - The wavelength (redshifted)                      = 6562.78 angstroms
# Interference order:
#      - The interference order @ 6562.78                 = 609.498 
#      - The interference order @ 6598.95                 = 606.157 
#      - The interference order @ 6562.78                 = 609.498 
# Free Spectral Range :
#      - The FSR @ 6598.95 in wavelength                  = 10.8866 Angstrom
#      - The FSR @ 6562.78 in wavelength                  = 10.7675 Angstrom
#      - The FSR @ 6562.78 in thickness                   = 0.328139 microns 
#      - The FSR @ 6562.78 in wavelength                  = 10.7675 Angstrom
#      - The FSR @ 6562.78 in km/s                        = 491.869 km/s
#      - The queensgate constant QGC                      = 18.3304 Angstrom
#      - The FSR in BCV @ 6562.78A                        = 358.027
#      - The FSR in BCV @ 6562.78A                        = 358.027
#      - The FSR in BCV @ 6598.95A                        = 360
# Finesse & Scanning:
#      - You gave a real finesse                         = 21.95
#      - Shannon sampling of the finesse                 = 2
#      - Considering F=21.95 and the sampling =2, the float nb of ch to scan for one FSR  = 43.9
#      - Considering F=21.95 and FSR=10.7675, the spectral sampling = 0.490549 Angstroms
#      - The spectral Resolution @ 6562.78 Angstroms        = 13378
#      - The average number of BCV for one FSR             = 8.1555
#      - The maximum number of BCV that the CS100 can jump at once = 3
# Overscanning:
#      - You wanted to scan                                 = 1.1 FSR 
#      - The BCV gap that will be scanned @ 6562.78 Angstro = 393.829
#      - The total number of channels that will be scanned  = 49
#      - The initial BCV value   (nfiniz)                   = 2600
#      - The final BCV value should be around (nfiniz_end)  = 2208.54
# SAMI:
#      - You gave nsweeps  = 1
#      - You gave nsteps   = 1
#      - You gave nframe   = 1
#      - You gave exptim per channel             = 120 seconds
#      - Readout time per exposure               = 3 seconds 
#      - Total exposure time (whole observation) = 100.45 minutes
#      - Total exposure time (whole observation) = 1.67417 hours
#      - You gave binxy                          = 4 
#      - You gave the basename                   = scan_005A

set dat = `date +%Y-%m-%dT%H:%M:%S`
set scid = "SCAN_$dat"
echo "SCAN $scid"
set sweepkey = "FAPERSWP"
set stepkey = "FAPERSST"
set scankey = "FAPERSID"
set nsweeps = 1
set nsteps = 1
set nframe = 1
set nfiniz = 2600
set exptim = 120.0
set binxy = 4
set basename = "scan_005A"
set cmd = `sami dhe set image.dir /home2/images/SAMFP/20170723/005`
set cmd = `sami dhe dbs set $scankey $scid`
set cmd = `sami dhe dbs set $stepkey custom`
echo "setting number of images, exposure time and basename"
sami dhe set binning $binxy $binxy
sami dhe set obs.nimages $nframe
sami dhe set obs.exptime $exptim
sami dhe set image.basename $basename
echo
echo "image $basename, exptime $exptim"
echo "binning $binxy"
echo
echo "moving FP to channel 1: BCV=2600"
sami FP moveabs 2600
set sweepid = C001
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 1)"
sami dhe expose
echo
echo "moving FP to BCV 2597 "
sami FP moveabs 2597
sleep 1
echo
echo "moving FP to BCV 2594 "
sami FP moveabs 2594
sleep 1
echo
echo "moving FP to channel 2: BCV=2592"
sami FP moveabs 2592
set sweepid = C002
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 2)"
sami dhe expose
echo
echo "moving FP to BCV 2589 "
sami FP moveabs 2589
sleep 1
echo
echo "moving FP to BCV 2586 "
sami FP moveabs 2586
sleep 1
echo
echo "moving FP to channel 3: BCV=2584"
sami FP moveabs 2584
set sweepid = C003
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 3)"
sami dhe expose
echo
echo "moving FP to BCV 2581 "
sami FP moveabs 2581
sleep 1
echo
echo "moving FP to BCV 2578 "
sami FP moveabs 2578
sleep 1
echo
echo "moving FP to channel 4: BCV=2576"
sami FP moveabs 2576
set sweepid = C004
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 4)"
sami dhe expose
echo
echo "moving FP to BCV 2573 "
sami FP moveabs 2573
sleep 1
echo
echo "moving FP to BCV 2570 "
sami FP moveabs 2570
sleep 1
echo
echo "moving FP to channel 5: BCV=2567"
sami FP moveabs 2567
set sweepid = C005
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 5)"
sami dhe expose
echo
echo "moving FP to BCV 2564 "
sami FP moveabs 2564
sleep 1
echo
echo "moving FP to BCV 2561 "
sami FP moveabs 2561
sleep 1
echo
echo "moving FP to channel 6: BCV=2559"
sami FP moveabs 2559
set sweepid = C006
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 6)"
sami dhe expose
echo
echo "moving FP to BCV 2556 "
sami FP moveabs 2556
sleep 1
echo
echo "moving FP to BCV 2553 "
sami FP moveabs 2553
sleep 1
echo
echo "moving FP to channel 7: BCV=2551"
sami FP moveabs 2551
set sweepid = C007
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 7)"
sami dhe expose
echo
echo "moving FP to BCV 2548 "
sami FP moveabs 2548
sleep 1
echo
echo "moving FP to BCV 2545 "
sami FP moveabs 2545
sleep 1
echo
echo "moving FP to channel 8: BCV=2543"
sami FP moveabs 2543
set sweepid = C008
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 8)"
sami dhe expose
echo
echo "moving FP to BCV 2540 "
sami FP moveabs 2540
sleep 1
echo
echo "moving FP to BCV 2537 "
sami FP moveabs 2537
sleep 1
echo
echo "moving FP to channel 9: BCV=2535"
sami FP moveabs 2535
set sweepid = C009
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 9)"
sami dhe expose
echo
echo "moving FP to BCV 2532 "
sami FP moveabs 2532
sleep 1
echo
echo "moving FP to BCV 2529 "
sami FP moveabs 2529
sleep 1
echo
echo "moving FP to channel 10: BCV=2527"
sami FP moveabs 2527
set sweepid = C010
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 10)"
sami dhe expose
echo
echo "moving FP to BCV 2524 "
sami FP moveabs 2524
sleep 1
echo
echo "moving FP to BCV 2521 "
sami FP moveabs 2521
sleep 1
echo
echo "moving FP to channel 11: BCV=2518"
sami FP moveabs 2518
set sweepid = C011
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 11)"
sami dhe expose
echo
echo "moving FP to BCV 2515 "
sami FP moveabs 2515
sleep 1
echo
echo "moving FP to BCV 2512 "
sami FP moveabs 2512
sleep 1
echo
echo "moving FP to channel 12: BCV=2510"
sami FP moveabs 2510
set sweepid = C012
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 12)"
sami dhe expose
echo
echo "moving FP to BCV 2507 "
sami FP moveabs 2507
sleep 1
echo
echo "moving FP to BCV 2504 "
sami FP moveabs 2504
sleep 1
echo
echo "moving FP to channel 13: BCV=2502"
sami FP moveabs 2502
set sweepid = C013
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 13)"
sami dhe expose
echo
echo "moving FP to BCV 2499 "
sami FP moveabs 2499
sleep 1
echo
echo "moving FP to BCV 2496 "
sami FP moveabs 2496
sleep 1
echo
echo "moving FP to channel 14: BCV=2494"
sami FP moveabs 2494
set sweepid = C014
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 14)"
sami dhe expose
echo
echo "moving FP to BCV 2491 "
sami FP moveabs 2491
sleep 1
echo
echo "moving FP to BCV 2488 "
sami FP moveabs 2488
sleep 1
echo
echo "moving FP to channel 15: BCV=2486"
sami FP moveabs 2486
set sweepid = C015
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 15)"
sami dhe expose
echo
echo "moving FP to BCV 2483 "
sami FP moveabs 2483
sleep 1
echo
echo "moving FP to BCV 2480 "
sami FP moveabs 2480
sleep 1
echo
echo "moving FP to channel 16: BCV=2478"
sami FP moveabs 2478
set sweepid = C016
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 16)"
sami dhe expose
echo
echo "moving FP to BCV 2475 "
sami FP moveabs 2475
sleep 1
echo
echo "moving FP to BCV 2472 "
sami FP moveabs 2472
sleep 1
echo
echo "moving FP to channel 17: BCV=2470"
sami FP moveabs 2470
set sweepid = C017
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 17)"
sami dhe expose
echo
echo "moving FP to BCV 2467 "
sami FP moveabs 2467
sleep 1
echo
echo "moving FP to BCV 2464 "
sami FP moveabs 2464
sleep 1
echo
echo "moving FP to channel 18: BCV=2461"
sami FP moveabs 2461
set sweepid = C018
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 18)"
sami dhe expose
echo
echo "moving FP to BCV 2458 "
sami FP moveabs 2458
sleep 1
echo
echo "moving FP to BCV 2455 "
sami FP moveabs 2455
sleep 1
echo
echo "moving FP to channel 19: BCV=2453"
sami FP moveabs 2453
set sweepid = C019
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 19)"
sami dhe expose
echo
echo "moving FP to BCV 2450 "
sami FP moveabs 2450
sleep 1
echo
echo "moving FP to BCV 2447 "
sami FP moveabs 2447
sleep 1
echo
echo "moving FP to channel 20: BCV=2445"
sami FP moveabs 2445
set sweepid = C020
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 20)"
sami dhe expose
echo
echo "moving FP to BCV 2442 "
sami FP moveabs 2442
sleep 1
echo
echo "moving FP to BCV 2439 "
sami FP moveabs 2439
sleep 1
echo
echo "moving FP to channel 21: BCV=2437"
sami FP moveabs 2437
set sweepid = C021
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 21)"
sami dhe expose
echo
echo "moving FP to BCV 2434 "
sami FP moveabs 2434
sleep 1
echo
echo "moving FP to BCV 2431 "
sami FP moveabs 2431
sleep 1
echo
echo "moving FP to channel 22: BCV=2429"
sami FP moveabs 2429
set sweepid = C022
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 22)"
sami dhe expose
echo
echo "moving FP to BCV 2426 "
sami FP moveabs 2426
sleep 1
echo
echo "moving FP to BCV 2423 "
sami FP moveabs 2423
sleep 1
echo
echo "moving FP to channel 23: BCV=2421"
sami FP moveabs 2421
set sweepid = C023
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 23)"
sami dhe expose
echo
echo "moving FP to BCV 2418 "
sami FP moveabs 2418
sleep 1
echo
echo "moving FP to BCV 2415 "
sami FP moveabs 2415
sleep 1
echo
echo "moving FP to channel 24: BCV=2412"
sami FP moveabs 2412
set sweepid = C024
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 24)"
sami dhe expose
echo
echo "moving FP to BCV 2409 "
sami FP moveabs 2409
sleep 1
echo
echo "moving FP to BCV 2406 "
sami FP moveabs 2406
sleep 1
echo
echo "moving FP to channel 25: BCV=2404"
sami FP moveabs 2404
set sweepid = C025
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 25)"
sami dhe expose
echo
echo "moving FP to BCV 2401 "
sami FP moveabs 2401
sleep 1
echo
echo "moving FP to BCV 2398 "
sami FP moveabs 2398
sleep 1
echo
echo "moving FP to channel 26: BCV=2396"
sami FP moveabs 2396
set sweepid = C026
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 26)"
sami dhe expose
echo
echo "moving FP to BCV 2393 "
sami FP moveabs 2393
sleep 1
echo
echo "moving FP to BCV 2390 "
sami FP moveabs 2390
sleep 1
echo
echo "moving FP to channel 27: BCV=2388"
sami FP moveabs 2388
set sweepid = C027
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 27)"
sami dhe expose
echo
echo "moving FP to BCV 2385 "
sami FP moveabs 2385
sleep 1
echo
echo "moving FP to BCV 2382 "
sami FP moveabs 2382
sleep 1
echo
echo "moving FP to channel 28: BCV=2380"
sami FP moveabs 2380
set sweepid = C028
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 28)"
sami dhe expose
echo
echo "moving FP to BCV 2377 "
sami FP moveabs 2377
sleep 1
echo
echo "moving FP to BCV 2374 "
sami FP moveabs 2374
sleep 1
echo
echo "moving FP to channel 29: BCV=2372"
sami FP moveabs 2372
set sweepid = C029
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 29)"
sami dhe expose
echo
echo "moving FP to BCV 2369 "
sami FP moveabs 2369
sleep 1
echo
echo "moving FP to BCV 2366 "
sami FP moveabs 2366
sleep 1
echo
echo "moving FP to channel 30: BCV=2363"
sami FP moveabs 2363
set sweepid = C030
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 30)"
sami dhe expose
echo
echo "moving FP to BCV 2360 "
sami FP moveabs 2360
sleep 1
echo
echo "moving FP to BCV 2357 "
sami FP moveabs 2357
sleep 1
echo
echo "moving FP to channel 31: BCV=2355"
sami FP moveabs 2355
set sweepid = C031
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 31)"
sami dhe expose
echo
echo "moving FP to BCV 2352 "
sami FP moveabs 2352
sleep 1
echo
echo "moving FP to BCV 2349 "
sami FP moveabs 2349
sleep 1
echo
echo "moving FP to channel 32: BCV=2347"
sami FP moveabs 2347
set sweepid = C032
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 32)"
sami dhe expose
echo
echo "moving FP to BCV 2344 "
sami FP moveabs 2344
sleep 1
echo
echo "moving FP to BCV 2341 "
sami FP moveabs 2341
sleep 1
echo
echo "moving FP to channel 33: BCV=2339"
sami FP moveabs 2339
set sweepid = C033
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 33)"
sami dhe expose
echo
echo "moving FP to BCV 2336 "
sami FP moveabs 2336
sleep 1
echo
echo "moving FP to BCV 2333 "
sami FP moveabs 2333
sleep 1
echo
echo "moving FP to channel 34: BCV=2331"
sami FP moveabs 2331
set sweepid = C034
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 34)"
sami dhe expose
echo
echo "moving FP to BCV 2328 "
sami FP moveabs 2328
sleep 1
echo
echo "moving FP to BCV 2325 "
sami FP moveabs 2325
sleep 1
echo
echo "moving FP to channel 35: BCV=2323"
sami FP moveabs 2323
set sweepid = C035
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 35)"
sami dhe expose
echo
echo "moving FP to BCV 2320 "
sami FP moveabs 2320
sleep 1
echo
echo "moving FP to BCV 2317 "
sami FP moveabs 2317
sleep 1
echo
echo "moving FP to channel 36: BCV=2315"
sami FP moveabs 2315
set sweepid = C036
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 36)"
sami dhe expose
echo
echo "moving FP to BCV 2312 "
sami FP moveabs 2312
sleep 1
echo
echo "moving FP to BCV 2309 "
sami FP moveabs 2309
sleep 1
echo
echo "moving FP to channel 37: BCV=2306"
sami FP moveabs 2306
set sweepid = C037
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 37)"
sami dhe expose
echo
echo "moving FP to BCV 2303 "
sami FP moveabs 2303
sleep 1
echo
echo "moving FP to BCV 2300 "
sami FP moveabs 2300
sleep 1
echo
echo "moving FP to channel 38: BCV=2298"
sami FP moveabs 2298
set sweepid = C038
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 38)"
sami dhe expose
echo
echo "moving FP to BCV 2295 "
sami FP moveabs 2295
sleep 1
echo
echo "moving FP to BCV 2292 "
sami FP moveabs 2292
sleep 1
echo
echo "moving FP to channel 39: BCV=2290"
sami FP moveabs 2290
set sweepid = C039
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 39)"
sami dhe expose
echo
echo "moving FP to BCV 2287 "
sami FP moveabs 2287
sleep 1
echo
echo "moving FP to BCV 2284 "
sami FP moveabs 2284
sleep 1
echo
echo "moving FP to channel 40: BCV=2282"
sami FP moveabs 2282
set sweepid = C040
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 40)"
sami dhe expose
echo
echo "moving FP to BCV 2279 "
sami FP moveabs 2279
sleep 1
echo
echo "moving FP to BCV 2276 "
sami FP moveabs 2276
sleep 1
echo
echo "moving FP to channel 41: BCV=2274"
sami FP moveabs 2274
set sweepid = C041
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 41)"
sami dhe expose
echo
echo "moving FP to BCV 2271 "
sami FP moveabs 2271
sleep 1
echo
echo "moving FP to BCV 2268 "
sami FP moveabs 2268
sleep 1
echo
echo "moving FP to channel 42: BCV=2266"
sami FP moveabs 2266
set sweepid = C042
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 42)"
sami dhe expose
echo
echo "moving FP to BCV 2263 "
sami FP moveabs 2263
sleep 1
echo
echo "moving FP to BCV 2260 "
sami FP moveabs 2260
sleep 1
echo
echo "moving FP to channel 43: BCV=2257"
sami FP moveabs 2257
set sweepid = C043
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 43)"
sami dhe expose
echo
echo "moving FP to BCV 2254 "
sami FP moveabs 2254
sleep 1
echo
echo "moving FP to BCV 2251 "
sami FP moveabs 2251
sleep 1
echo
echo "moving FP to channel 44: BCV=2249"
sami FP moveabs 2249
set sweepid = C044
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 44)"
sami dhe expose
echo
echo "moving FP to BCV 2246 "
sami FP moveabs 2246
sleep 1
echo
echo "moving FP to BCV 2243 "
sami FP moveabs 2243
sleep 1
echo
echo "moving FP to channel 45: BCV=2241"
sami FP moveabs 2241
set sweepid = C045
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 45)"
sami dhe expose
echo
echo "moving FP to BCV 2238 "
sami FP moveabs 2238
sleep 1
echo
echo "moving FP to BCV 2235 "
sami FP moveabs 2235
sleep 1
echo
echo "moving FP to channel 46: BCV=2233"
sami FP moveabs 2233
set sweepid = C046
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 46)"
sami dhe expose
echo
echo "moving FP to BCV 2230 "
sami FP moveabs 2230
sleep 1
echo
echo "moving FP to BCV 2227 "
sami FP moveabs 2227
sleep 1
echo
echo "moving FP to channel 47: BCV=2225"
sami FP moveabs 2225
set sweepid = C047
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 47)"
sami dhe expose
echo
echo "moving FP to BCV 2222 "
sami FP moveabs 2222
sleep 1
echo
echo "moving FP to BCV 2219 "
sami FP moveabs 2219
sleep 1
echo
echo "moving FP to channel 48: BCV=2217"
sami FP moveabs 2217
set sweepid = C048
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 48)"
sami dhe expose
echo
echo "moving FP to BCV 2214 "
sami FP moveabs 2214
sleep 1
echo
echo "moving FP to BCV 2211 "
sami FP moveabs 2211
sleep 1
echo
echo "moving FP to channel 49: BCV=2209"
sami FP moveabs 2209
set sweepid = C049
set cmd = `sami dhe dbs set $sweepkey $sweepid`
sami dhe set image.basename $basename"_"$sweepid
echo "SWEEP $sweepid"
echo "taking data...(sweep $sweepid step 49)"
sami dhe expose
# Channel: +Step ==> BCV
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
# [0, -8, -8, -8, -9, -8, -8, -8, -8, -8, -9, -8, -8, -8, -8, -8, -8, -9, -8, -8, -8, -8, -8, -9, -8, -8, -8, -8, -8, -9, -8, -8, -8, -8, -8, -8, -9, -8, -8, -8, -8, -8, -9, -8, -8, -8, -8, -8, -8]
# [2600, 2592, 2584, 2576, 2567, 2559, 2551, 2543, 2535, 2527, 2518, 2510, 2502, 2494, 2486, 2478, 2470, 2461, 2453, 2445, 2437, 2429, 2421, 2412, 2404, 2396, 2388, 2380, 2372, 2363, 2355, 2347, 2339, 2331, 2323, 2315, 2306, 2298, 2290, 2282, 2274, 2266, 2257, 2249, 2241, 2233, 2225, 2217, 2209]
