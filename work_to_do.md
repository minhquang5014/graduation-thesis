This file will write down all the TO-DO work that must be done in 2 weeks: 

1. The interface is almost done. 

2. Problem with holding register 17, 18, 19, 20 - done

3. Problem with the sending signal to PLC holding reg 0, 1, 2, 3, it should update periodically - done

4. Capture the image of the products
Here is the logic of it:
Try to read signal from the PLC, from the holding registers numbers from 34-37
If there is anything enabled (only holding register from 0 to 1), it will capture the image, save the image in the working directory, give it a name, and then return the name
Update the second frame with the recognized objects
Using root.after to check the signal periodically, and update the GUI smoothly without blocking the detection

Check list:
- Lighting system is okay on the third frame
- start, stop buttons are oke, sending signal to PLC
- Lights for start and stop are okay, turning green and red 