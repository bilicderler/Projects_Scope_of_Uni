using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class Snake : MonoBehaviour
{
    public List<Transform> tail = new List<Transform>();

    public List<string> TrueWords = new List<string>();
    public List<string> FalseWords = new List<string>();

    public GameObject A, B, C, D;
    public GameController gameController;

    public SpriteRenderer spriteRenderer;
    public Sprite RHead,LHead,DHead,UHead;


    public GameObject SnakeBody1;
    public GameObject SnakeBody2;

    public GameObject EffectTrue,EffectFalse;

    public int count;
    public int x;

    Vector2 dir = Vector2.zero;//herhangi bir y�ne ba�latmak i�in vector2.right/left vs yap�labilir

    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        InvokeRepeating("Move", 0.1f, 0.4f);//her 0.3 bekletip 0.3 sn'de bir move fonksiyonunu �al��t�r�r.
    }

    void Update()
    {
       
        if (Input.GetKey(KeyCode.RightArrow))
        {
            if(this.name == "SnakeHead")
            {
                spriteRenderer.sprite = LHead;
                
            }
  
            dir = Vector2.right;
            Time.timeScale = 1;
            x = 6;
        }
           
        else if (Input.GetKey(KeyCode.DownArrow))
        {
            if (this.name == "SnakeHead")
            {
                spriteRenderer.sprite = DHead;

            }
      
            dir = -Vector2.up;
            Time.timeScale = 1;

            x = 2;
        }
        else if (Input.GetKey(KeyCode.LeftArrow))
        {
            if (this.name == "SnakeHead")
            {
                spriteRenderer.sprite = RHead;

            }
    
            dir = -Vector2.right;
            Time.timeScale = 1;
            x = 4;
        }
        else if (Input.GetKey(KeyCode.UpArrow))
        {
            if (this.name == "SnakeHead")
            {
                spriteRenderer.sprite = UHead;

            }

            dir = Vector2.up;
            Time.timeScale = 1;
            x = 8;
        }

        if (Input.GetKey(KeyCode.Space))
        {

            Time.timeScale = 0;
        }

    }

    void Move()
    {
        Vector2 poz = transform.position;

        transform.Translate(dir);//Translate dir in vector2 ye g�re hareketini uygular

        if (tail.Count > 0)
        {
            if(x == 8)
            {
                tail.Last().position =new Vector2(poz.x,poz.y + 0.5f);
            }
            else if(x == 6)
            {
                tail.Last().position = new Vector2(poz.x+0.6f, poz.y);

            }
            else if (x == 4)
            {
                tail.Last().position = new Vector2(poz.x - 0.6f, poz.y);

            }
            else if (x == 2)
            {
                tail.Last().position = new Vector2(poz.x, poz.y-0.5f);

            }
            // tail.Last().position = poz; //arkadaki kuyru�u kafan�n son pozisyonuna e�itliyoruz

            tail.Insert(0, tail.Last());// �ndekinin pozisyonuna kuyruk ekliyoruz. 
            tail.RemoveAt(tail.Count - 1);// ve arkada kalan kuyru�u siliyoruz

        }
    }



    void OnTriggerEnter2D(Collider2D coll)
    {
        if (this.name == "SnakeHead")
        {
            if (coll.name == "Wall")
            {
                transform.position = new Vector3(7.176f, transform.position.y, transform.position.z);
            }
            else if (coll.name == "Wall1")
            {
                transform.position = new Vector3(-8.2f, transform.position.y, transform.position.z);
            }
            else if (coll.name == "Wall2")
            {
                transform.position = new Vector3(transform.position.x, 2.24f, transform.position.z);
            }
            else if (coll.name == "Wall3")
            {
                transform.position = new Vector3(transform.position.x, -4.27f, transform.position.z);
            }


            if (coll.name == "Dogru")
            {
                Destroy(Instantiate(EffectTrue, new Vector3(transform.position.x, transform.position.y, -5), Quaternion.identity),2f);
                
                A.SetActive(false);
                B.SetActive(false);
                C.SetActive(false);
                D.SetActive(false);

                GameController.Score += 2; //Skor artar
                gameController.ScoreText.text = GameController.Score.ToString(); // Score int de�erini stringe �evirip texte e�itledik

                gameController.ChangeBackGround();//de�i�en skor say�s�na g�re arka plan� de�i�tirmek i�in fonksiyonu �a��rd�k

                TrueWords.Add(gameController.EnWordText.text);//Do�ru kelimeyi truewords e ekliyoruz


                gameController.EnWordsList.RemoveAt(gameController.RandomInt);
                gameController.TrueWordsList.RemoveAt(gameController.RandomInt);

                StartCoroutine(GenerateNewWords());//Fonksiyonu ge�iktirmek i�in �zel bir coroutine fonksiyonu �a��r�yoruz
            }
            else if (coll.name == "A" || coll.name == "B" || coll.name == "C" || coll.name == "D")
            {
                Destroy(Instantiate(EffectFalse, new Vector3(transform.position.x,transform.position.y,-5), Quaternion.identity), 2f);


                A.SetActive(false);
                B.SetActive(false);
                C.SetActive(false);
                D.SetActive(false);

                GameController.Score--;
                gameController.ScoreText.text = GameController.Score.ToString(); //skor text her de�i�ti�inde g�ncellenmeli

                gameController.ChangeBackGround();//de�i�en skor say�s�na g�re arka plan� de�i�tirmek i�in fonksiyonu �a��rd�k

                gameController.RepeatingFalse.Add(gameController.EnWordText.text);

                StartCoroutine(GenerateNewWords());
            }
        }

    }


    public IEnumerator GenerateNewWords() // Coroutine i�inde �a��rd���m�z fonksiyon.
    {
        //S�reyi azaltmak i�in 
        gameController.a.GetComponent<SpriteRenderer>().name = "A";
        gameController.b.GetComponent<SpriteRenderer>().name = "B";
        gameController.c.GetComponent<SpriteRenderer>().name = "C";
        gameController.d.GetComponent<SpriteRenderer>().name = "D";

        gameController.RandomQuestion();

        yield return new WaitForSeconds(3f);// i�erisine girilen float de�er kadar kodu o noktada bekletir
        
        

        A.SetActive(true);
        B.SetActive(true);
        C.SetActive(true);
        D.SetActive(true);

        yield break;
    }

}