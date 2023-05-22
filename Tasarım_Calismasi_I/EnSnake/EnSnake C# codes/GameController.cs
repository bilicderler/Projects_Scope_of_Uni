using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;


public class GameController : MonoBehaviour
{
    [Header("Lists")]
    public List<string> EnWordsList;
    public List<string> TrueWordsList;
    public List<string> RepeatingFalse;
    public List<string> ShowRepeatingFalse;


    [Header("Arrays")]
    public string[] EnWords;    //sorulacak ingilizce kelimeler için
    public string[] TrueWords; // Doðru Türkçe kelimeler için
    public string[] RandomWords; //Random yanlýþ Türkçe kelime dizisi
    public string[] Choice; //þýklar dizisi(a,b,c,d)

    [Header("Int Objs")]
    public int RandomInt, RandomInt2, RandomInt3, RandomInt4, RandomInt5;
    public static int Score = 0; //static ile baþka kod üzerinden verilen önceki deðeri deðiþtirebiliriz.
    int bg; // background deðiþtirme kontrolü



    [Header("Game Objects")]
    public GameObject a, b, c, d;
    public GameObject Bg1, Bg2, Bg3, Bg4, Bg5;
    public GameObject EndGameScreen; // Siyah Ekran Objesi
    public GameObject SnakeHeadObj;


    [Header("Texts")]
    public Text EnWordText, ScoreText, LiveScoreText,ShowTrueWordsText, ShowFalseWordsText,ShowRepeatingFalseText;
    public Text AText, BText, CText, DText;

    public Snake snake;
    private int count,count2;

    public object EnWordt { get; internal set; }

    public void Start()
    {
       
        if (LiveScoreText != null)
        {
Invoke("RandomQuestion", 0.1f);
        }
        
    }
    void Update()
    {
        if(LiveScoreText != null)
        {
            LiveScoreText.text = Score.ToString();
        }

    }
    public void RandomQuestion()
    {
        CheckGameScore();
        CheckGameEnd();

        RandomInt = Random.Range(0, EnWordsList.Count);//random.range(0,5); 0 ile 4 dahil olduðu deðerleri döndürür +1 yap dene
        EnWordText.text = EnWordsList[RandomInt];

        RandomInt2 = Random.Range(0, 4);

        Invoke("ChangeTrueWordsName", 0.5f); //Random sayýnýn gelesini beklettik. 


        switch (Choice[RandomInt2])
        {

            case "D":
                {
                    DText.text = TrueWordsList[RandomInt];
                    RandomInt3 = Random.Range(0, RandomWords.Length);
                    RandomInt4 = Random.Range(0, RandomWords.Length);
                    RandomInt5 = Random.Range(0, RandomWords.Length);


                    BText.text = RandomWords[RandomInt3];
                    CText.text = RandomWords[RandomInt4];
                    AText.text = RandomWords[RandomInt5]; break;
                }
            case "C":
                {
                    CText.text = TrueWordsList[RandomInt];
                    RandomInt3 = Random.Range(0, RandomWords.Length);
                    RandomInt4 = Random.Range(0, RandomWords.Length);
                    RandomInt5 = Random.Range(0, RandomWords.Length);
                    

                    BText.text = RandomWords[RandomInt3];
                    AText.text = RandomWords[RandomInt4];
                    DText.text = RandomWords[RandomInt5]; break;
                }
            case "A":
                {
                    AText.text = TrueWordsList[RandomInt];
                    RandomInt3 = Random.Range(0, RandomWords.Length);
                    RandomInt4 = Random.Range(0, RandomWords.Length);
                    RandomInt5 = Random.Range(0, RandomWords.Length);


                    BText.text = RandomWords[RandomInt3];
                    CText.text = RandomWords[RandomInt4];
                    DText.text = RandomWords[RandomInt5]; ; break;
                }
            case "B":
                {
                    BText.text = TrueWordsList[RandomInt];
                    RandomInt3 = Random.Range(0, RandomWords.Length);
                    RandomInt4 = Random.Range(0, RandomWords.Length);
                    RandomInt5 = Random.Range(0, RandomWords.Length);


                    AText.text = RandomWords[RandomInt3];
                    CText.text = RandomWords[RandomInt4];
                    DText.text = RandomWords[RandomInt5]; ; break;
                }
        }

        while (Choice[RandomInt2] == "A" && BText.text == CText.text || BText.text == DText.text || CText.text == DText.text || AText.text == BText.text || AText.text == CText.text || AText.text == DText.text)
        {

            //AText.text = TrueWordsList[RandomInt];
            BText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            CText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            DText.text = RandomWords[Random.Range(0, RandomWords.Length)];
        }
        while (Choice[RandomInt2] == "B" && AText.text == CText.text || AText.text == DText.text || CText.text == DText.text || BText.text == AText.text || BText.text == CText.text || BText.text == DText.text)
        {

            //BText.text = TrueWordsList[RandomInt];
            CText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            AText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            DText.text = RandomWords[Random.Range(0, RandomWords.Length)];
        }
        while (Choice[RandomInt2] == "C" && AText.text == BText.text || AText.text == DText.text || BText.text == DText.text || CText.text == AText.text || CText.text == BText.text || CText.text == DText.text)
        {

            //CText.text = TrueWordsList[RandomInt];
            BText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            AText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            DText.text = RandomWords[Random.Range(0, RandomWords.Length)];
        }
        while (Choice[RandomInt2] == "D" && AText.text == CText.text || BText.text == CText.text || AText.text == BText.text || DText.text == AText.text || DText.text == CText.text || DText.text == BText.text)
        {

           // DText.text = TrueWordsList[RandomInt];
            BText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            CText.text = RandomWords[Random.Range(0, RandomWords.Length)];
            AText.text = RandomWords[Random.Range(0, RandomWords.Length)];
        }
    }
    void ChangeTrueWordsName()
    {
       // Debug.Log(Choice[RandomInt2]);
       // Debug.Log(TrueWordsList[RandomInt]);

        if (Choice[RandomInt2] == "A")
        {
            AText.text = TrueWordsList[RandomInt];

            a.GetComponent<SpriteRenderer>().name = "Dogru";
        }
        else if (Choice[RandomInt2] == "B")
        {
            BText.text = TrueWordsList[RandomInt];

            b.GetComponent<SpriteRenderer>().name = "Dogru";
        }
        else if (Choice[RandomInt2] == "C")
        {
            CText.text = TrueWordsList[RandomInt];
            c.GetComponent<SpriteRenderer>().name = "Dogru";

        }
        else if(Choice[RandomInt2] == "D")
        {
            DText.text = TrueWordsList[RandomInt];
            d.GetComponent<SpriteRenderer>().name = "Dogru";
        }
    }
    public void CheckGameScore() // oyun skorla bitsin istiyosak burayý deðiþtiricez
    {
        if (Score < 0)
        {
            Score = 0;
            ScoreText.text = Score.ToString();
            //OYUNU DURACAK VE SKOR EKRANI AÇILACAK
            SnakeHeadObj.SetActive(false);
            Time.timeScale = 0;


            for (int i = 0; i < RepeatingFalse.Count; i++)
            {
                count = 0;
                for (int j = 0; j < RepeatingFalse.Count; j++)
                {
                    if (RepeatingFalse[i] == RepeatingFalse[j])
                    {
                        count++;
                    }

                    //ekle yeni listeye
                }
                if (count == 1)
                {
                    snake.FalseWords.Add(RepeatingFalse[i]);
                }
                else if (count > 1)
                {                  
                        count2 = 0;
                        for (int l = 0; l < ShowRepeatingFalse.Count; l++)
                        {
                            if (RepeatingFalse[i] == ShowRepeatingFalse[l])
                            {
                                count2++;
                            }
                        }
                        if (count2 == 0)
                        {
                            ShowRepeatingFalse.Add(RepeatingFalse[i]);
                        }
                        
                }
            }
            // Oyun sonu ekranýna kelimeler yazdýrýlýr
            for (int i = 0; i < snake.TrueWords.Count; i++)
            {
                ShowTrueWordsText.text += snake.TrueWords[i] + ("\n");
            }
            for (int j = 0; j < snake.FalseWords.Count; j++)
            {
                ShowFalseWordsText.text += snake.FalseWords[j] + ("\n");
            }
            for (int k = 0; k < ShowRepeatingFalse.Count; k++)
            {
                ShowRepeatingFalseText.text += ShowRepeatingFalse[k] + ("\n");
            }

            EndGameScreen.SetActive(true);
        }
    }
   public void ChangeBackGround()
    {

        if(Score >= 0 && Score < 10)
        {
            Bg1.SetActive(true);
            Bg2.SetActive(false);
        }
        else if (Score >= 10 && Score <20 /*&& bg == 0*/){ 
            bg++;
            if (Bg3.activeInHierarchy == true) {
                Bg3.SetActive(false);
            }

            Bg1.SetActive(false);
            Bg2.SetActive(true);
        }
        else if (Score >= 20 && Score < 30 /*&& bg == 1*/)
        {
            bg++;

            if (Bg4.activeInHierarchy == true)
            {
                Bg4.SetActive(false);
            }
            Bg2.SetActive(false);
            Bg3.SetActive(true);
        }
        else if (Score >= 30 && Score < 40 /*&& bg == 2*/)
        {

            if (Bg5.activeInHierarchy == true)
            {
                Bg5.SetActive(false);
            }
            bg++;
            Bg3.SetActive(false);
            Bg4.SetActive(true);
        }
        else if (Score >= 40 && Score < 50 /*&& bg == 3*/)
        {
            bg++;
            Bg4.SetActive(false);
            Bg5.SetActive(true);
        }
    }
   public void CheckGameEnd()
    {
        if (EnWordsList.Count <= 1)
        {
            Score = 0;

            SnakeHeadObj.SetActive(false);

            Time.timeScale = 0;//Oyun zamanýný durduruyoruz ve oyun yeniden baþlýycaksa Time.timeScale =1 ; yapmalýyýz;

            for (int i = 0; i < RepeatingFalse.Count; i++)
            {
                count = 0;
                for (int j = 0; j < RepeatingFalse.Count; j++)
                {
                    if (RepeatingFalse[i] == RepeatingFalse[j])
                    {
                        count++;
                    }

                    //ekle yeni listeye
                }
                if (count == 1)
                {
                    snake.FalseWords.Add(RepeatingFalse[i]);
                }
                else if (count > 1)
                {
                    count2 = 0;
                    for (int l = 0; l < ShowRepeatingFalse.Count; l++)
                    {
                        if (RepeatingFalse[i] == ShowRepeatingFalse[l])
                        {
                            count2++;
                        }
                    }
                    if (count2 == 0)
                    {
                        ShowRepeatingFalse.Add(RepeatingFalse[i]);
                    }

                }
            }




            for (int i =0;i< snake.TrueWords.Count;i++)
            {
                ShowTrueWordsText.text += snake.TrueWords[i]+("\n"); 
            }
            for (int j =0; j<snake.FalseWords.Count; j++)
            {
                ShowFalseWordsText.text += snake.FalseWords[j] + ("\n");
            }
            for(int k=0;k<ShowRepeatingFalse.Count;k++)
            {
                ShowRepeatingFalseText.text += ShowRepeatingFalse[k] + ("\n");
            }

                EndGameScreen.SetActive(true);



        }
    }
    public void ExitButtn()
    {
        Application.Quit();
    }
    public void PlayAgain()
    {
        SceneManager.LoadScene("OpenScene");

    }
}
