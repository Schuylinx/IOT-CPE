package com.example.iot_project;

import android.os.AsyncTask;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;


import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

/**
 *
 * Classe permettant la gestion des réceptions UDP
 *
 */
public class ReceiverTask extends AsyncTask<Void, byte[], Void> {

    // Instanciation des variables liées à la socket
    private DatagramSocket UDPSocket;

    // Instance de la MainActivity
    private MainActivity MaFenetre;

    /**
     * Constructeur de la classe, bind entre les deux classes
     * @param UDPSocket
     * @param MaFenetre
     */
    public ReceiverTask(DatagramSocket UDPSocket, MainActivity MaFenetre) {
        this.UDPSocket = UDPSocket;
        this.MaFenetre = MaFenetre;
    }

    /**
     * Extension de AsyncTask, surcharge
     * @param voids
     * @return
     */
    @Override
    protected Void doInBackground(Void... voids) {
        while(true){
            byte[] data = new byte [1024];
            DatagramPacket packet = new DatagramPacket(data, data.length);
            try {
                UDPSocket.receive(packet);
                int size = packet.getLength();
                publishProgress(java.util.Arrays.copyOf(data, size));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * Extension de AsyncTask, surcharge
     *
     * @param data
     */
    @Override
    protected void onProgressUpdate(byte[]... data) {

        String value = new String(data[0]);
        try {
            JSONObject monObjet = new JSONObject(value);
            JSONArray tab = (JSONArray)((monObjet.get("data")));
            String valueTemperature = (String)tab.get(0);
            String valueLight = (String)tab.get(1);
            MaFenetre.setValues(valueTemperature,valueLight);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}