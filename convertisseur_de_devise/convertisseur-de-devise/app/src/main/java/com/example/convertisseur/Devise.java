package com.example.convertisseur;


public class Devise {
    public String nom;
    public double dollar_coeff;
    public int drapeau;
    public String logo;
    public int id;

    public Devise(int id, String nom, double dollar_coeff, int drapeau, String logo){
        this.id = id;
        this.nom=nom;
        this.dollar_coeff=dollar_coeff;
        this.drapeau=drapeau;
        this.logo=logo;
    }

}
