package com.example.convertisseur;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.ArrayList;

import android.view.View;


public class MainActivity extends AppCompatActivity {

    static String devise_depart = "";
    static String devise_arrivee = "";
    static double coef= 1;
    static double coef_entre = 1.01;
    static double coef_sortie = 1;
    static int drap_entree = R.drawable.eu_flag;
    static int drap_sortie = R.drawable.flag_usa;
    static String logo_devise_arrive = "€";
    static String logo_devise_depart ="$";
    static int id_depart = 0;
    static int id_arrivee = 1;

    Spinner spinner_depart;
    Spinner spinner_arrivee;

    SpinnerActivity SA_0 = new SpinnerActivity(0);
    SpinnerActivity SA_1 = new SpinnerActivity(1);

    Devise EU = new Devise(0,"Euro",1.01,R.drawable.eu_flag, "€");
    Devise USA = new Devise(1,"Dollar USA", 1,R.drawable.flag_usa, "$");
    Devise Chine = new Devise(2,"Yuan", 7.3,R.drawable.flag_china, "元");
    Devise Japon = new Devise(3,"Yen", 148.61,R.drawable.flag_japan,"¥");

    public static ArrayList<Devise> Devises = new ArrayList<Devise>();

    Devise devise_d = EU;
    Devise devise_a = USA;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Création de la liste des devises
        Devises.add(EU);
        Devises.add(USA);
        Devises.add(Chine);
        Devises.add(Japon);

        /* ------------ Spinner ----------- */
        spinner_depart = (Spinner) findViewById(R.id.devises_depart);
        //écouteur du spinner
        spinner_depart.setOnItemSelectedListener(SA_0);
        spinner_depart.setSelection(id_depart);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> adapter_depart = ArrayAdapter.createFromResource(this,
                R.array.devises_depart, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        adapter_depart.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        spinner_depart.setAdapter(adapter_depart);

        ArrayAdapter<CharSequence> adapter_arrivee = ArrayAdapter.createFromResource(this,
                R.array.devises_arrivee, android.R.layout.simple_spinner_item);
        adapter_arrivee.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner_arrivee = (Spinner) findViewById(R.id.devises_arrivee);
        // Apply the adapter to the spinner
        spinner_arrivee.setAdapter(adapter_arrivee);
        //écouteur du spinner
        spinner_arrivee.setOnItemSelectedListener(SA_1);
        spinner_arrivee.setSelection(id_arrivee);


    }


    public void ajouter(String s){
        devise_depart += s;

        TextView t = (TextView) findViewById(R.id.valeur_devise_depart);
        t.setText(devise_depart);

        convertir();
    }

    public void convertir(){

        coef = coef_sortie/coef_entre;
        double v = Double.valueOf(devise_depart) * coef;


        DecimalFormat df = new DecimalFormat("###.##");
        devise_arrivee = df.format(v);

        //valeur à échanger
        TextView t = (TextView) findViewById(R.id.valeur_devise_arrivee);
        t.setText(devise_arrivee);

        // gestion drapeau
        ImageView I_e =(ImageView) findViewById(R.id.drapeau_depart);
        I_e.setImageResource(drap_entree);
        ImageView I_s =(ImageView) findViewById(R.id.drapeau_arrive);
        I_s.setImageResource(drap_sortie);

        //gestion logo devise
        TextView l_d = (TextView) findViewById(R.id.logo_devise_depart);
        l_d.setText(logo_devise_depart);
        TextView l_a = (TextView) findViewById(R.id.logo_devise_arrivee);
        l_a.setText(logo_devise_arrive);
    }

    public void echange(){
        //var de stockage
        double coef_entre_stock = coef_entre;
        int drap_entre_stock = drap_entree;
        String devise_départ_stock = devise_depart;
        String logo_devise_depart_stock = logo_devise_depart;
        int id_stock = id_depart;

        //échange départ
        coef_entre = coef_sortie;
        drap_entree = drap_sortie;
        devise_depart = devise_arrivee;
        logo_devise_depart = logo_devise_arrive;
        id_depart = id_arrivee;

        TextView t_d = (TextView) findViewById(R.id.valeur_devise_depart);
        t_d.setText(devise_depart);
        ImageView I_e =(ImageView) findViewById(R.id.drapeau_depart);
        I_e.setImageResource(drap_entree);
        TextView l_d = (TextView) findViewById(R.id.logo_devise_depart);
        l_d.setText(logo_devise_depart);
        spinner_depart.setSelection(id_arrivee);


        //échange arrivée
        coef_sortie = coef_entre_stock;
        drap_sortie =drap_entre_stock;
        devise_arrivee  =devise_départ_stock;
        logo_devise_arrive = logo_devise_depart_stock;
        id_arrivee = id_stock;
        TextView t = (TextView) findViewById(R.id.valeur_devise_arrivee);
        t.setText(devise_arrivee);
        ImageView I_s =(ImageView) findViewById(R.id.drapeau_arrive);
        I_s.setImageResource(drap_sortie);
        TextView l_a = (TextView) findViewById(R.id.logo_devise_arrivee);
        l_a.setText(logo_devise_arrive);
        spinner_arrivee.setSelection(id_stock);


    }

    public void supprimer(){
        // Séparation pour la gestion de l'erreur: devise_depart = ""
        if (devise_depart.length()>1) {
            int l = devise_depart.length();
            devise_depart = devise_depart.substring(0,(l-1));
            if (devise_depart.charAt(devise_depart.length()-1)!='.') convertir();
            TextView t_d = (TextView) findViewById(R.id.valeur_devise_depart);
            t_d.setText(devise_depart);
        }
        else{
            devise_depart="";
            devise_arrivee="";
            TextView t = (TextView) findViewById(R.id.valeur_devise_arrivee);
            t.setText("0");
            TextView t_d = (TextView) findViewById(R.id.valeur_devise_depart);
            t_d.setText("0");
        }

    }

    public void point(){
        int l = devise_depart.length();
        if (l>=1){
            if (devise_depart.charAt(l-1)!='.'){
                devise_depart+=".";
            }
        }
        else devise_depart="0.";
        TextView t_d = (TextView) findViewById(R.id.valeur_devise_depart);
        t_d.setText(devise_depart);
    }

    /* ----------- Gestion du Clavier ----------- */
    public void fonctionBouton(View view){

        System.out.println(logo_devise_depart);
        System.out.println(logo_devise_arrive);

        if (view.getId() == R.id.bouton_1) ajouter("1");
        if (view.getId() == R.id.bouton_2) ajouter("2");
        if (view.getId() == R.id.bouton_3) ajouter("3");
        if (view.getId() == R.id.bouton_4) ajouter("4");
        if (view.getId() == R.id.bouton_5) ajouter("5");
        if (view.getId() == R.id.bouton_6) ajouter("6");
        if (view.getId() == R.id.bouton_7) ajouter("7");
        if (view.getId() == R.id.bouton_8) ajouter("8");
        if (view.getId() == R.id.bouton_9) ajouter("9");
        if (view.getId() == R.id.bouton_10) point();
        if (view.getId() == R.id.bouton_11) ajouter("0");
        if (view.getId() == R.id.bouton_12) supprimer();
        if (view.getId() == R.id.bouton_echange) echange();

        System.out.println(logo_devise_depart);
        System.out.println(logo_devise_arrive);

    }



    //----------- getteur ---------------
    public  static ArrayList<Devise> getDevises(){
        return Devises;
    }

    public static double getCoef_entre(){
        return coef_entre;
    }

    public static double getCoef(){
        return coef;
    }

    public static double getCoef_sortie(){
        return coef_sortie;
    }

    public static String getDevise_depart(){
        return devise_depart;
    }

    public static String getDevise_arrivee(){
        return devise_arrivee;
    }


    // --------------- setteur ---------------------
    public static  void setCoef_entree(double c){
        coef_entre=c;
    }

    public static  void setCoef_sortie(double c){
        coef_sortie=c;
    }

    public static  void setDrapeau_entree(int drapeau){
        drap_entree=drapeau;
    }

    public static  void setDrapeau_sortie(int drapeau){
        drap_sortie=drapeau;
    }

    public static void setLogo_devise_arrive(String logo){
        logo_devise_arrive=logo;
    }
    public static void setLogo_devise_depart(String logo){
        logo_devise_depart=logo;
    }

    public static void setId_depart(int id){
        id_depart=id;
    }

    public static void setId_arrivee(int id){
        id_arrivee=id;
    }
}
