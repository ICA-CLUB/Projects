// ConsoleDiceRoller.java
import java.util.*;

import java.io.*;
import javax.imageio.ImageIO;
import javax.sound.sampled.*;
import javax.swing.*;
import java.awt.image.BufferedImage;
import java.awt.*;
import javax.swing.Timer;


public class ConsoleDiceRoller {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        Random random = new Random();
        int numofdice;
        int total = 0;

        System.out.println(" Welcome to Console Dice Roller!");

        System.out.print("Enter the number of dice to roll: ");

        numofdice = scan.nextInt();

        if (numofdice > 0) {
            for (int i = 0; i < numofdice; i++) {
                int roll = random.nextInt(6) + 1;
                System.out.println("You rolled: " + roll);
                total += roll;
                playSound("assets_diceroller_final/roll.wav");
                showDiceImage("assets_diceroller_final/dice" + roll + ".png", roll);
            }

            System.out.println("Total of dice rolled: " + total);
        }
         else {
            System.out.println("Invalid number of dice. Please enter a number greater than 0.");
        }
        credits();

        scan.close();
    }

    // Method to play sound
    public static void playSound(String soundFilePath) {
        try {
            File soundFile = new File(soundFilePath);
            if (soundFile.exists()) {
                AudioInputStream audioInput = AudioSystem.getAudioInputStream(soundFile);
                Clip clip = AudioSystem.getClip();
                clip.open(audioInput);
                clip.start();
                Thread.sleep(1000); // Wait for 1 second
            } else {
                System.out.println("Sound file not found: " + soundFilePath);
            }
        } catch (Exception e) {
            System.out.println("Error playing sound.");
            e.printStackTrace();
        }
    }

    // Method to show image in a new window
   
        public static void showDiceImage(String imagePath, int roll) {
    try {
        File imgFile = new File(imagePath);
        System.out.println("Trying to load image: " + imagePath); // Debug print
        if (imgFile.exists()) {
            BufferedImage img = ImageIO.read(imgFile);
            ImageIcon icon = new ImageIcon(img);

            JFrame frame = new JFrame(" Dice Roll: " + roll);
            JLabel label = new JLabel(icon);
            frame.add(label);
            frame.setSize(500, 500);
            frame.setLocationRelativeTo(null);
            frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            frame.setVisible(true);

            // Use javax.swing.Timer to auto-close window after 2 seconds
            javax.swing.Timer timer = new javax.swing.Timer(2000, e -> frame.dispose());
            timer.setRepeats(false);
            timer.start();
        } else {
            System.out.println(" Image file not found: " + imagePath);
        }
    } catch (IOException e) {
        System.out.println(" Error showing dice image for roll " + roll);
        e.printStackTrace();
    }
}



    // scenario logics for practice
    public static void sampleDelay() {
        for (int i = 0; i < 5; i++) {
            System.out.println("Simulating delay: " + (i + 1));
        }
    }

    public static void printDiceFaceArt(int roll) {
        String[] faces = {
            "-----\n|   |\n| o |\n|   |\n-----",
            "-----\n|o  |\n|   |\n|  o|\n-----",
            "-----\n|o  |\n| o |\n|  o|\n-----",
            "-----\n|o o|\n|   |\n|o o|\n-----",
            "-----\n|o o|\n| o |\n|o o|\n-----",
            "-----\n|o o|\n|o o|\n|o o|\n-----"
        };
        System.out.println("Dice face:\n" + faces[roll - 1]);
    }

    public static void debugInfo(int roll) {
        System.out.println("[DEBUG] Roll value: " + roll);
        System.out.println("[DEBUG] Timestamp: " + System.currentTimeMillis());
    }

    public static void greetings() {
        System.out.println("Thanks for playing Dice Roller!");
    }

    public static void credits() {
        System.out.println("Created by Vaishnavee and Kratika ");
    }

    // Call these extras 
    public static void extraFun(int roll) {
        printDiceFaceArt(roll);
        debugInfo(roll);
        greetings();
        credits();
        sampleDelay();
    }
}
