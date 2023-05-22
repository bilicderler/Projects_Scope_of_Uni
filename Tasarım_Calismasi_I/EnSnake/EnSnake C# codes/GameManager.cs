using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
public class GameManager : MonoBehaviour
{
    public GameController gameController;
    
    public Text ShowTrueWordsText, ShowEnWordsText;

    private void Start()
    {
        StartCoroutine(WriteWords());
    }

    
    public void StartGameBtn()
    {
        SceneManager.LoadScene("SampleScene");
    }
        
    IEnumerator  WriteWords()
    {
        yield return new WaitForSeconds(0.1f);

        for (int i = 0; i < gameController.EnWords.Length; i++)
        {
            ShowEnWordsText.text += gameController.EnWords[i] + (" ------------> \n");
            ShowTrueWordsText.text += gameController.TrueWords[i] + (" \n");

        }

        yield break;
    }
}
