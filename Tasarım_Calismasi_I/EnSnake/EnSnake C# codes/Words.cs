using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Words : MonoBehaviour
{
    public GameController gameController;
    public void Start()
    {
        gameController.EnWords = new string[] {  "Swim" , "Walk" ,"Read","Shout","Get", "Steal", "Adjective",
             "Air" ,"Answer" ,"Anything", "Abroad" , "Accept" , "Accident"  ,"Achievement" , "Add"  ,
             "Adult"  ,"Adventure","Again","Airport","And", "Angry","Anybody-Anyone ", "Appearance" ,
            "Arrive","Ask","Atmosphere","Attend", "Guest", "Grow", "Hair" , "Handsome","Field","Virtual"};

        gameController.TrueWords = new string[] { "Y�zmek", "Y�r�mek" , "Okumak", "Ba��rmak" , "Almak", "�almak", "S�fat", "Hava", "Cevap",
            "Hi�bir �ey", "Yurtd���", "Kabul Etmek", "Kaza", "Ba�ar�", "Eklemek" , "Yeti�kin", "Macera", "Tekrar",
            "Havaliman�", "Ve", "K�zg�n","Hi� Kimse", "G�r�n��", "Varmak", "Sormak", "Atmosfer", "Kat�lmak", "Misafir", "B�y�mek", "Sa�" ,"Yak���kl�","Alan","Sanal"};

        gameController.EnWordsList = new List<string>(gameController.EnWords);
        gameController.TrueWordsList = new List<string>(gameController.TrueWords);


        gameController.RepeatingFalse = new List<string> {};
        gameController.ShowRepeatingFalse = new List<string>{};


        gameController.RandomWords = new string[] { "Yakalamak","Takmak","Sevmek","Dolmak", "�ptal etmek", "D�v��", "Uygun", "Y�zmek", "Y�r�mek", "Okumak", "Ba��rmak", "Almak", "�almak", "S�fat", "Hava", "Cevap",
            "Hi�bir �ey", "Yurtd���", "Kabul Etmek", "Kaza", "Ba�ar�", "Eklemek", "Yeti�kin", "Macera", "Tekrar", "Havaliman�", "Ve", "K�zg�n", "Hi� Kimse", "G�r�n��", "Varmak", "Sormak",
            "Atmosfer", "Kat�lmak", "Takip","Delirmek","�z�lmek","Mutlu","�a�k�n" };


        gameController.Choice = new string[] { "A", "B", "C", "D" };
    }
}
