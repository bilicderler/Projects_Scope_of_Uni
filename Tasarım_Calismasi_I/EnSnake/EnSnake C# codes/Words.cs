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

        gameController.TrueWords = new string[] { "Yüzmek", "Yürümek" , "Okumak", "Baðýrmak" , "Almak", "Çalmak", "Sýfat", "Hava", "Cevap",
            "Hiçbir Þey", "Yurtdýþý", "Kabul Etmek", "Kaza", "Baþarý", "Eklemek" , "Yetiþkin", "Macera", "Tekrar",
            "Havalimaný", "Ve", "Kýzgýn","Hiç Kimse", "Görünüþ", "Varmak", "Sormak", "Atmosfer", "Katýlmak", "Misafir", "Büyümek", "Saç" ,"Yakýþýklý","Alan","Sanal"};

        gameController.EnWordsList = new List<string>(gameController.EnWords);
        gameController.TrueWordsList = new List<string>(gameController.TrueWords);


        gameController.RepeatingFalse = new List<string> {};
        gameController.ShowRepeatingFalse = new List<string>{};


        gameController.RandomWords = new string[] { "Yakalamak","Takmak","Sevmek","Dolmak", "Ýptal etmek", "Dövüþ", "Uygun", "Yüzmek", "Yürümek", "Okumak", "Baðýrmak", "Almak", "Çalmak", "Sýfat", "Hava", "Cevap",
            "Hiçbir Þey", "Yurtdýþý", "Kabul Etmek", "Kaza", "Baþarý", "Eklemek", "Yetiþkin", "Macera", "Tekrar", "Havalimaný", "Ve", "Kýzgýn", "Hiç Kimse", "Görünüþ", "Varmak", "Sormak",
            "Atmosfer", "Katýlmak", "Takip","Delirmek","Üzülmek","Mutlu","Þaþkýn" };


        gameController.Choice = new string[] { "A", "B", "C", "D" };
    }
}
