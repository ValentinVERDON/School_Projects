package com.example.convertisseur;


import static com.example.convertisseur.MainActivity.id_arrivee;
import static com.example.convertisseur.MainActivity.id_depart;
import static com.example.convertisseur.MainActivity.setCoef_entree;
import static com.example.convertisseur.MainActivity.setCoef_sortie;
import static com.example.convertisseur.MainActivity.setDrapeau_entree;
import static com.example.convertisseur.MainActivity.setDrapeau_sortie;
import static com.example.convertisseur.MainActivity.setId_arrivee;
import static com.example.convertisseur.MainActivity.setId_depart;
import static com.example.convertisseur.MainActivity.setLogo_devise_arrive;
import static com.example.convertisseur.MainActivity.setLogo_devise_depart;

import android.app.Activity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.convertisseur.MainActivity;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class SpinnerActivity extends Activity implements AdapterView.OnItemSelectedListener {
    public int id;
    private TextView t;
    private TextView l_d;
    private TextView l_a;
    private ImageView I_e;
    private ImageView I_s;


    /* Identitifant pour repérer entré/sortie */
    public SpinnerActivity(int id){
        this.id = id;
        System.out.println(id);
    }

    /* Trouver la devise sélectionée */
    public Devise find_devises(String t) {
        ArrayList<Devise> Devises = MainActivity.getDevises();
        int l = Devises.size();
        int i=0;
        Devise d = new Devise(id = 0,"erreur",0,0,"€");
        while (i < l) {
            if (Devises.get(i).nom.equals(t)) {
                d = Devises.get(i);
            }
            i++;
        }
        return d;
    }

    /* Action lorsqu'on sélectionne un item */
    public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
        // On récupère l'item
        String t = (String) parent.getItemAtPosition(pos);
        //Ici, il faut chercher la devise correspondante
        Devise d = find_devises(t);
        // Cas spinner entrée
        if (id==0){
            setCoef_entree(d.dollar_coeff);
           setDrapeau_entree(d.drapeau);
           setLogo_devise_depart(d.logo);
           setId_depart(d.id);
           System.out.println("id depart : " + id_depart);
        }

        // Cas spinner sortie
        else{
            setCoef_sortie(d.dollar_coeff);
            setDrapeau_sortie(d.drapeau);
            setLogo_devise_arrive(d.logo);
            setId_arrivee(d.id);
            System.out.println("id depart : " + id_arrivee);
        }
    }

    public void onNothingSelected(AdapterView<?> parent) {
        // Another interface callback
    }

}
