package cpe.moi.projet_iot;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

/**
 *
 * Classe pilote de l'application
 *
 */
public class MainActivity extends AppCompatActivity {

    final int REFRESH_TIME = 10000;

    // Instanciation des variables liées à l'IHM
    private Button btnStart;
    private TextView lib1, lib2, edit2, edit1, editLog;
    private EditText editIp, editPort;
    private Switch switchTL;
    private boolean socketCreated;

    // Instanciation des variables liées à la socket
    private int port;
    private InetAddress address;
    private DatagramSocket UDPSocket;

    // Variable pour la gestion de l'affichage, si = 1, le programme est lancé, sinon il est arrêté
    private boolean applicationStarted = false;

    /**
     * Méthode appelée à l'initation de la fênetre
     *
     * Initialisation de l'interface IHM, des listeners sur les boutons, de la socket UDP
     *
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialisation des éléments IHM
        initIHM();

        // Listener sur le bouton Start
        btnStart.setOnClickListener(new OnClickListener() {
            public void onClick(View v) {

                // Création de la socket d'envoi, gestion de l'exception si problème lors de la création
                socketCreated = initSocket();

                if (socketCreated) {

                    // Création de la socket d'écoute
                    (new ReceiverTask(UDPSocket, MainActivity.this)).execute();

                    // Si l'application est lancée, on active le rafraichissement automatique des valeurs
                    if (applicationStarted) {
                        editLog.append("----- Arrêt du programme -----\n");
                        btnStart.setText("START");
                        editIp.setEnabled(true);
                        editPort.setEnabled(true);
                    } else {
                        editLog.append("----- Mise à jour automatique des valeurs activée -----\n");
                        btnStart.setText("STOP");
                        editIp.setEnabled(false);
                        editPort.setEnabled(false);
                        (new Thread() {
                            public void run() {
                                while (applicationStarted) {
                                    try {
                                        sendData("getValues()");
                                        Thread.sleep(REFRESH_TIME);
                                    } catch (InterruptedException e) {
                                        e.printStackTrace();
                                    }
                                }
                            }
                        }).start();
                    }
                    applicationStarted = !applicationStarted;
                }
            }
        });

        // Listener sur le switch de sélection de l'ordre d'affichage des données
        switchTL.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    sendData("LT");
                    editLog.append("Passage en mode LT\n");
                } else {
                    sendData("TL");
                    editLog.append("Passage en mode TL\n");
                }
                editLog.append("Changement du mode d'affichage, récupération des dernières valeurs...\n");
                sendData("getValues()");
            }
        });
    }

    /**
     * Méthode appelée à l'envoi de données vers la passerelle
     *
     * @param data String tableau a deux dimensions, valeurs possibles :
     *             - "GetValues()", ""
     *             - "LT", ""
     *             - "TL", ""
     */
    private void sendData(final String data){
        (new Thread() {
            public void run() {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        editLog.append("Envoi de la donnée : " + data + "\n");
                    }
                });

                try {
                    byte[] transmittedData = (formattingDataSent(data)).getBytes();
                    DatagramPacket packet = new DatagramPacket(transmittedData, transmittedData.length, address, port);
                    UDPSocket.send(packet);
                    Thread.sleep(REFRESH_TIME);
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                    editLog.append("Problème lors de l'émission du packet UDP vers la passerelle...\n");
                }
            }
        }).start();
    }

    /**
     * Méthode de création d'une socket
     *
     * Gestion d'exception si problème lors de la création
     *
     * @return true si la socket a été créée avec succès
     *         false si la création de la socket a échouée
     */
    private boolean initSocket(){
        try {
            UDPSocket = new DatagramSocket();
            address = InetAddress.getByName(editIp.getText().toString());
            editLog.append("Socket créée\n");
        } catch (SocketException | UnknownHostException var3) {
            editLog.append("Impossible de créer la socket...\n");
            var3.printStackTrace();
            return false;
        }
        port = Integer.parseInt(editPort.getText().toString());
        return true;
    }

    /**
     * Initialisation du contenu des champs
     */
    private void initConnexionIHM(){
        editIp.setText("10.0.2.2");
        editPort.setText("10000");
    }

    /**
     * Initialisation des éléments IHM
     */
    private void initIHM(){
        btnStart = (Button)findViewById(R.id.Button_Start);
        lib1 = (TextView)findViewById(R.id.Label_Temperature);
        lib2 = (TextView)findViewById(R.id.Label_Light);
        edit1 = (TextView)findViewById(R.id.TextBox_Temperature);
        edit2 = (TextView)findViewById(R.id.TextBox_Light);
        editIp = (EditText)findViewById(R.id.TextBox_IP);
        editPort = (EditText)findViewById(R.id.TextBox_Port);
        editLog = (TextView)findViewById(R.id.TextViewTextMultiLine);
        // Affichage et défilement  automatique des logs
        editLog.setMovementMethod(new ScrollingMovementMethod());
        switchTL = (Switch)findViewById(R.id.Switch_TL);
        // Auto-Complétion des champs pour la connexion au serveur
        this.initConnexionIHM();
    }

    /**
     * Formattage en JSON des données envoyées à la passerelle
     *
     * @param data String tableau a deux dimensions, valeurs possibles :
     *      - "GetValues()", ""
     *      - "LT", ""
     *      - "TL", ""
     *
     * @return String formatée en JSON
     */
    private String formattingDataSent(String data){
        return "{\"source\":\"T\",\"destination\":\"P\",\"password\":\"ASecurePa$$19989/9\",\"data\":[\""+data+"\",\"\"]}";
    }

    /**
     * Méthode permettant de binder l'affichage en fonction de la séléction utilisateur
     *
     * @param temperatureValue String contenant la valeur de la température du capteur
     * @param lightValue String contenant la valeur de l'intensite lumineuse du capteur
     */
    public void setValues(String temperatureValue, String lightValue){
        if (switchTL.isChecked()){
            lib1.setText("Température en °C");
            lib2.setText("Intensité de la Lumière");
            edit1.setText(temperatureValue);
            edit2.setText(lightValue);
        } else {
            lib2.setText("Température en °C");
            lib1.setText("Intensité de la Lumière");
            edit2.setText(temperatureValue);
            edit1.setText(lightValue);
        }
    }

}