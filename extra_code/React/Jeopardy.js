import React, { useState, useEffect } from 'react';

// Main App component
const App = () => {
  // Game states
  const [gameState, setGameState] = useState('categorySelectionR1'); // 'categorySelectionR1', 'mainGameR1', 'categorySelectionR2', 'mainGameR2', 'dailyDoubleWager', 'dailyDoubleQuestion', 'dailyDoubleReveal', 'finalJeopardyWager', 'finalJeopardyQuestion', 'finalJeopardyReveal', 'gameOver'
  const [player1Score, setPlayer1Score] = useState(0);
  const [player2Score, setPlayer2Score] = useState(0);
  const [currentPlayer, setCurrentPlayer] = useState(1); // Player who chooses next question in main game
  const [buzzedInPlayer, setBuzzedInPlayer] = useState(null); // Player who buzzed in for the current question (main game)
  const [currentQuestion, setCurrentQuestion] = useState(null); // Stores the question object when selected (main game)
  const [showAnswer, setShowAnswer] = useState(false); // Controls showing the correct answer in regular questions
  const [message, setMessage] = useState(''); // For displaying messages like "Correct!" or "Incorrect!"
  const [userAnswer, setUserAnswer] = useState(''); // State to store the user's typed answer

  // States for category selection and loading
  const [selectedCategoriesR1, setSelectedCategoriesR1] = useState([]);
  const [selectedCategoriesR2, setSelectedCategoriesR2] = useState([]);
  const [newCategoryInput, setNewCategoryInput] = useState('');
  const [isLoadingQuestions, setIsLoadingQuestions] = useState(false);
  const [errorGenerating, setErrorGenerating] = useState('');

  // Game data for each round
  const [generatedGameDataR1, setGeneratedGameDataR1] = useState([]);
  const [generatedGameDataR2, setGeneratedGameDataR2] = useState([]);

  // Final Jeopardy states
  const [finalJeopardyCategory, setFinalJeopardyCategory] = useState('');
  const [finalJeopardyClue, setFinalJeopardyClue] = useState('');
  const [finalJeopardyAnswer, setFinalJeopardyAnswer] = useState('');
  const [player1Wager, setPlayer1Wager] = useState('');
  const [player2Wager, setPlayer2Wager] = useState('');
  const [player1FinalAnswer, setPlayer1FinalAnswer] = useState('');
  const [player2FinalAnswer, setPlayer2FinalAnswer] = useState('');
  const [player1FinalCorrect, setPlayer1FinalCorrect] = useState(null); // true/false/null
  const [player2FinalCorrect, setPlayer2FinalCorrect] = useState(null); // true/false/null
  const [finalAnswersRevealedCount, setFinalAnswersRevealedCount] = useState(0); // To track when both players have revealed

  // Daily Double states
  const [dailyDoubleQuestionDetails, setDailyDoubleQuestionDetails] = useState(null); // Stores the DD question object
  const [dailyDoubleWagerAmount, setDailyDoubleWagerAmount] = useState('');

  // Rebound state for regular questions
  const [isSecondChance, setIsSecondChance] = useState(false);
  const [originalBuzzer, setOriginalBuzzer] = useState(null); // Player who buzzed in first

  // Gemini API related states for hints
  const [generatedHint, setGeneratedHint] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [isGeneratingHint, setIsGeneratingHint] = useState(false);

  // Helper function to calculate Levenshtein distance between two strings
  const levenshteinDistance = (s1, s2) => {
    s1 = s1.toLowerCase();
    s2 = s2.toLowerCase();

    const costs = [];
    for (let i = 0; i <= s1.length; i++) {
      let lastValue = i;
      for (let j = 0; j <= s2.length; j++) {
        if (i === 0) {
          costs[j] = j;
        } else if (j > 0) {
          let newValue = costs[j - 1];
          if (s1.charAt(i - 1) !== s2.charAt(j - 1)) {
            newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
          }
          costs[j - 1] = lastValue;
          lastValue = newValue;
        }
      }
      if (i > 0) {
        costs[s2.length] = lastValue;
      }
    }
    return costs[s2.length];
  };

  // Helper function to clean strings for comparison
  const cleanStringForComparison = (str) => {
    let cleaned = str.toLowerCase().trim();
    // Remove Jeopardy-style question prefixes and question marks
    cleaned = cleaned.replace(/^(who is|what is|where is|when is)\s*/, '');
    cleaned = cleaned.replace(/\?$/, '');

    // Remove common articles and prepositions that might vary
    const stopWords = new Set(['a', 'an', 'the', 'is', 'of', 'in', 'on', 'at', 'for', 'with', 'to', 'from', 'by', 'and', 'or', 'but', 'that', 'this', 'these', 'those', 'are']);
    const words = cleaned.split(/\s+/).filter(word => !stopWords.has(word) && word.length > 0);
    return words.join(' ');
  };

  // Map of common names to their variations (nicknames, full names)
  const nameVariationsMap = {
    "robert": ["bob", "rob", "bobby"],
    "william": ["bill", "billy", "will"],
    "elizabeth": ["liz", "lizzy", "beth", "betty"],
    "thomas": ["tom", "tommy"],
    "richard": ["dick", "rich", "ricky"],
    "james": ["jim", "jimmy"],
    "john": ["jack", "johnny"],
    "charles": ["chuck", "charlie"],
    "margaret": ["peggy", "maggie"],
    "patricia": ["pat", "patti"],
    "edward": ["ed", "eddie", "ted", "teddy"],
    "frank": ["francis"],
    "joseph": ["joe", "joey"],
    "michael": ["mike", "mickey"],
    "david": ["dave", "davy"],
    "christopher": ["chris"],
    "daniel": ["dan", "danny"],
    "matthew": ["matt"],
    "alexander": ["alex", "alec"],
    "stephen": ["steve", "steven"],
    "catherine": ["kate", "katie"],
    "nicholas": ["nick"],
    "samuel": ["sam"],
    "anthony": ["tony"],
    "benjamin": ["ben", "benny"],
    "victoria": ["vicky"],
    "barbara": ["barb", "barbie"],
    "kenneth": ["ken", "kenny"],
    "gregory": ["greg"],
    "jeffrey": ["jeff"],
    "donald": ["don", "donny"],
    "ronald": ["ron", "ronny"],
    "andrew": ["andy", "drew"],
    "christina": ["chris", "tina"],
    "jennifer": ["jen", "jenny"],
    "susan": ["sue", "susie"],
    "timothy": ["tim"],
    "virginia": ["ginny"],
    "walter": ["walt"],
    "vincent": ["vince"],
    "leonard": ["lenny"],
    "arthur": ["art", "artie"],
    "george": ["georgie"], // Added for George Washington example
    "washington": [], // To ensure 'Washington' is also considered a valid part
  };

  // Function to get all variations for a name part
  const getAllNameVariations = (namePart) => {
    const variations = new Set([namePart]); // Start with the original name part
    // Check if the namePart is a canonical name (key in map)
    if (nameVariationsMap[namePart]) {
      nameVariationsMap[namePart].forEach(v => variations.add(v));
    }
    // Check if the namePart is a nickname (value in map)
    for (const canonicalName in nameVariationsMap) {
      if (nameVariationsMap[canonicalName].includes(namePart)) {
        variations.add(canonicalName);
        nameVariationsMap[canonicalName].forEach(v => variations.add(v)); // Add all variations of the canonical name
      }
    }
    return Array.from(variations); // Return unique variations as an array
  };

  // Function to add a category to the selection list for the current round
  const addCategory = () => {
    const trimmedCategory = newCategoryInput.trim();
    if (trimmedCategory) {
      if (gameState === 'categorySelectionR1' && !selectedCategoriesR1.includes(trimmedCategory.toUpperCase())) {
        setSelectedCategoriesR1([...selectedCategoriesR1, trimmedCategory.toUpperCase()]);
      } else if (gameState === 'categorySelectionR2' && !selectedCategoriesR2.includes(trimmedCategory.toUpperCase())) {
        setSelectedCategoriesR2([...selectedCategoriesR2, trimmedCategory.toUpperCase()]);
      }
      setNewCategoryInput('');
    }
  };

  // Function to remove a category from the selection list for the current round
  const removeCategory = (categoryToRemove) => {
    if (gameState === 'categorySelectionR1') {
      setSelectedCategoriesR1(selectedCategoriesR1.filter(cat => cat !== categoryToRemove));
    } else if (gameState === 'categorySelectionR2') {
      setSelectedCategoriesR2(selectedCategoriesR2.filter(cat => cat !== categoryToRemove));
    }
  };

  // Check if all questions for a given game data set have been answered
  const checkAllQuestionsAnswered = (data) => {
    if (!data || data.length === 0) return false;

    for (const category of data) {
      for (const question of category.questions) {
        if (!question.answered) {
          return false;
        }
      }
    }
    return true;
  };

  // Function to generate questions for a specific round using AI
  const generateRoundQuestions = async (roundNumber, categoriesToGenerate) => {
    if (categoriesToGenerate.length === 0) {
      setErrorGenerating(`Please add at least one category for Round ${roundNumber}.`);
      return null;
    }

    setIsLoadingQuestions(true);
    setErrorGenerating('');
    const generatedData = [];
    const values = roundNumber === 1 ? [200, 400, 600, 800, 1000] : [400, 800, 1200, 1600, 2000];

    for (const category of categoriesToGenerate) {
      try {
        const prompt = `Generate 5 Jeopardy-style clues and their answers (in question format) for the category: ${category}. Each clue should have a different difficulty, corresponding to values ${values.join(', ')}. Provide the output as a JSON array of objects, where each object has 'question' (the clue), 'answer' (the Jeopardy response), and 'value' (the dollar amount) fields.`;

        const chatHistory = [];
        chatHistory.push({ role: "user", parts: [{ text: prompt }] });

        const payload = {
          contents: chatHistory,
          generationConfig: {
            responseMimeType: "application/json",
            responseSchema: {
              type: "ARRAY",
              items: {
                type: "OBJECT",
                properties: {
                  "question": { "type": "STRING" },
                  "answer": { "type": "STRING" },
                  "value": { "type": "NUMBER" }
                },
                required: ["question", "answer", "value"]
              }
            }
          }
        };

        const apiKey = ""; // Canvas will automatically provide it in runtime
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.candidates && result.candidates.length > 0 &&
            result.candidates[0].content && result.candidates[0].content.parts &&
            result.candidates[0].content.parts.length > 0) {
          const jsonString = result.candidates[0].content.parts[0].text;
          const questions = JSON.parse(jsonString);

          // Ensure questions are sorted by value and marked as not answered
          const sortedQuestions = questions
            .sort((a, b) => a.value - b.value)
            .map(q => ({ ...q, answered: false, isDailyDouble: false })); // Add isDailyDouble flag

          generatedData.push({ category: category, questions: sortedQuestions });
        } else {
          console.error("Unexpected API response structure:", result);
          setErrorGenerating(`Failed to generate questions for category: ${category}. Please try again.`);
          setIsLoadingQuestions(false);
          return null;
        }
      } catch (error) {
        console.error("Error generating questions for category:", category, error);
        setErrorGenerating(`Error generating questions for category: ${category}. ${error.message}`);
        setIsLoadingQuestions(false);
        return null;
      }
    }

    // Assign Daily Doubles
    const numDailyDoubles = roundNumber === 1 ? 1 : 2;
    let availableQuestionIndices = [];
    generatedData.forEach((cat, catIdx) => {
      cat.questions.forEach((q, qIdx) => {
        availableQuestionIndices.push({ catIdx, qIdx });
      });
    });

    // Shuffle and pick daily double locations
    for (let i = availableQuestionIndices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [availableQuestionIndices[i], availableQuestionIndices[j]] = [availableQuestionIndices[j], availableQuestionIndices[i]];
    }

    for (let i = 0; i < numDailyDoubles && i < availableQuestionIndices.length; i++) {
      const { catIdx, qIdx } = availableQuestionIndices[i];
      generatedData[catIdx].questions[qIdx].isDailyDouble = true;
    }

    setIsLoadingQuestions(false);
    return generatedData;
  };

  // Handles starting a round after category selection
  const handleStartRound = async (roundNumber) => {
    let data;
    if (roundNumber === 1) {
      data = await generateRoundQuestions(1, selectedCategoriesR1);
      if (data) {
        setGeneratedGameDataR1(data);
        setGameState('mainGameR1');
      }
    } else if (roundNumber === 2) {
      data = await generateRoundQuestions(2, selectedCategoriesR2);
      if (data) {
        setGeneratedGameDataR2(data);
        setGameState('mainGameR2');
      }
    }
  };

  // Generate Final Jeopardy question
  const generateFinalJeopardyQuestion = async () => {
    setIsLoadingQuestions(true);
    setErrorGenerating('');
    try {
      const prompt = `Generate one Final Jeopardy-style clue and its answer (in question format) for a general knowledge category. Provide the output as a JSON object with 'category', 'question' (the clue), and 'answer' (the Jeopardy response) fields.`;

      const chatHistory = [];
      chatHistory.push({ role: "user", parts: [{ text: prompt }] });

      const payload = {
        contents: chatHistory,
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "OBJECT",
            properties: {
              "category": { "type": "STRING" },
              "question": { "type": "STRING" },
              "answer": { "type": "STRING" }
            },
            required: ["category", "question", "answer"]
          }
        }
      };

      const apiKey = ""; // Canvas will automatically provide it in runtime
      const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (result.candidates && result.candidates.length > 0 &&
          result.candidates[0].content && result.candidates[0].content.parts &&
          result.candidates[0].content.parts.length > 0) {
        const jsonString = result.candidates[0].content.parts[0].text;
        const finalJeopardy = JSON.parse(jsonString);
        setFinalJeopardyCategory(finalJeopardy.category);
        setFinalJeopardyClue(finalJeopardy.question);
        setFinalJeopardyAnswer(finalJeopardy.answer);
        setGameState('finalJeopardyWager'); // Move to wager stage
      } else {
        console.error("Unexpected API response structure for Final Jeopardy:", result);
        setErrorGenerating('Failed to generate Final Jeopardy question. Please try again.');
      }
    } catch (error) {
      console.error("Error generating Final Jeopardy question:", error);
      setErrorGenerating(`Error generating Final Jeopardy question: ${error.message}`);
    } finally {
      setIsLoadingQuestions(false);
    }
  };

  // Function to handle a cell click (main game)
  const handleCellClick = (categoryIndex, questionIndex) => {
    const currentRoundData = gameState === 'mainGameR1' ? generatedGameDataR1 : generatedGameDataR2;
    const category = currentRoundData[categoryIndex];
    const question = category.questions[questionIndex];

    if (!question.answered) {
      // Mark the question as answered immediately to prevent re-clicking
      const newGameData = gameState === 'mainGameR1' ? [...generatedGameDataR1] : [...generatedGameDataR2];
      newGameData[categoryIndex].questions[questionIndex].answered = true;
      if (gameState === 'mainGameR1') {
        setGeneratedGameDataR1(newGameData);
      } else {
        setGeneratedGameDataR2(newGameData);
      }

      if (question.isDailyDouble) {
        setDailyDoubleQuestionDetails({ ...question, categoryIndex, questionIndex, round: (gameState === 'mainGameR1' ? 1 : 2) });
        setGameState('dailyDoubleWager');
        setDailyDoubleWagerAmount(''); // Clear previous wager
        setErrorGenerating(''); // Clear any previous errors
      } else {
        setCurrentQuestion({ ...question, categoryIndex, questionIndex });
        setShowAnswer(false);
        setMessage('');
        setUserAnswer('');
        setBuzzedInPlayer(null);
        setIsSecondChance(false); // Reset second chance for new question
        setOriginalBuzzer(null); // Reset original buzzer
        setGeneratedHint(''); // Reset hint
        setShowHint(false); // Hide hint
        setIsGeneratingHint(false); // Reset hint loading state
      }
    }
  };

  // Function for a player to buzz in (main game)
  const handleBuzzIn = (player) => {
    if (currentQuestion && buzzedInPlayer === null) {
      setBuzzedInPlayer(player);
      setMessage(`Player ${player} buzzed in!`);
      // If this is the first buzz for this question, set the original buzzer
      if (!isSecondChance) {
        setOriginalBuzzer(player);
      }
    }
  };

  // Function to check the user's typed answer (main game & Daily Double)
  const checkAnswer = () => {
    const questionToJudge = currentQuestion || dailyDoubleQuestionDetails;
    const playerToScore = buzzedInPlayer || currentPlayer; // For DD, it's always currentPlayer

    if (!questionToJudge || !playerToScore) return;

    const cleanedUserAnswer = cleanStringForComparison(userAnswer);
    let cleanedCorrectAnswer = cleanStringForComparison(questionToJudge.answer);

    const userWords = cleanedUserAnswer.split(' ').filter(word => word.length > 0);
    let correctWords = cleanedCorrectAnswer.split(' ').filter(word => word.length > 0);

    let isCorrect = false; // Assume incorrect unless proven otherwise

    // Enhanced logic for names (if the answer starts with "who is")
    if (questionToJudge.answer.toLowerCase().startsWith("who is")) {
      let expandedCorrectWords = new Set();
      correctWords.forEach(word => {
        // Get variations for each part of the correct name
        getAllNameVariations(word).forEach(variation => expandedCorrectWords.add(variation));
      });
      correctWords = Array.from(expandedCorrectWords); // Use the expanded set for comparison
    }

    // Now apply the fuzzy matching logic with the potentially expanded correctWords
    if (correctWords.length === 0) {
      isCorrect = userWords.length === 0;
    } else {
      // If user provided a single word, check if it matches any part of the correct answer or its variations
      if (userWords.length === 1) {
        const singleUserWord = userWords[0];
        for (const correctPart of correctWords) {
          const threshold = correctPart.length <= 3 ? 0 : (correctPart.length <= 6 ? 1 : 2);
          if (levenshteinDistance(correctPart, singleUserWord) <= threshold) {
            isCorrect = true;
            break;
          }
        }
      } else {
        // If user provided multiple words, check if all correct words have a close match in user's answer
        isCorrect = true; // Assume correct initially
        for (const correctWord of correctWords) {
          let foundMatch = false;
          const threshold = correctWord.length <= 3 ? 0 : (correctWord.length <= 6 ? 1 : 2);
          for (const userWord of userWords) {
            if (levenshteinDistance(correctWord, userWord) <= threshold) {
              foundMatch = true;
              break;
            }
          }
          if (!foundMatch) {
            isCorrect = false;
            break;
          }
        }
      }
    }

    let scoreChange = questionToJudge.value;
    if (questionToJudge.isDailyDouble) {
      scoreChange = parseInt(dailyDoubleWagerAmount);
    }

    if (isCorrect) {
      if (playerToScore === 1) {
        setPlayer1Score(prevScore => prevScore + scoreChange);
      } else {
        setPlayer2Score(prevScore => prevScore + scoreChange);
      }
      setMessage('Correct!');
      setShowAnswer(true); // Show answer and allow close
      // If correct, the player who answered correctly gets to choose next, so set currentPlayer to them
      setCurrentPlayer(playerToScore);
    } else {
      if (playerToScore === 1) {
        setPlayer1Score(prevScore => prevScore - scoreChange);
      } else {
        setPlayer2Score(prevScore => prevScore - scoreChange);
      }
      setMessage('Incorrect!');

      if (questionToJudge.isDailyDouble) {
        // Daily Double: no second chance, just switch player
        setShowAnswer(true);
        setCurrentPlayer(prevPlayer => (prevPlayer === 1 ? 2 : 1));
      } else if (!isSecondChance) {
        // Regular question, first attempt incorrect: give second chance
        setIsSecondChance(true);
        setBuzzedInPlayer(null); // Clear buzzer to allow other player to buzz in
        setMessage(`Incorrect! Player ${playerToScore === 1 ? 2 : 1} can now buzz in.`);
        setUserAnswer(''); // Clear input for next player
        setShowAnswer(false); // Don't show answer yet
      } else {
        // Regular question, second attempt incorrect: close question
        setShowAnswer(true);
        setMessage('Incorrect! No one got it right.');
        // Turn goes to the player who *didn't* get the second chance
        setCurrentPlayer(originalBuzzer === 1 ? 2 : 1);
      }
    }
  };

  // Function to reveal the answer without typing (main game & Daily Double)
  const revealAnswer = () => {
    const questionToJudge = currentQuestion || dailyDoubleQuestionDetails;
    const playerToScore = buzzedInPlayer || currentPlayer; // For DD, it's always currentPlayer

    if (!questionToJudge || !playerToScore) return;

    let scoreChange = questionToJudge.value;
    if (questionToJudge.isDailyDouble) {
      scoreChange = parseInt(dailyDoubleWagerAmount);
    }

    if (playerToScore === 1) {
      setPlayer1Score(prevScore => prevScore - scoreChange);
    } else {
      setPlayer2Score(prevScore => prevScore - scoreChange);
    }
    setMessage('Answer revealed! Points deducted.');
    setShowAnswer(true);

    if (questionToJudge.isDailyDouble) {
      // Daily Double: no second chance, just switch player
      setCurrentPlayer(prevPlayer => (prevPlayer === 1 ? 2 : 1));
    } else if (!isSecondChance) {
      // Regular question, first attempt revealed: give second chance
      setIsSecondChance(true);
      setBuzzedInPlayer(null); // Clear buzzer to allow other player to buzz in
      setMessage(`Answer revealed! Player ${playerToScore === 1 ? 2 : 1} can now buzz in.`);
      setUserAnswer(''); // Clear input for next player
      setShowAnswer(false); // Don't show answer yet
    } else {
      // Regular question, second attempt revealed: close question
      setMessage('Answer revealed! No one got it right.');
      // Turn goes to the player who *didn't* get the second chance
      setCurrentPlayer(originalBuzzer === 1 ? 2 : 1);
    }
  };

  // New function to handle passing a question
  const handlePass = () => {
    const questionToJudge = currentQuestion; // Pass only applies to regular questions
    const playerWhoPassed = buzzedInPlayer; // The player who chose to pass

    if (!questionToJudge || !playerWhoPassed) return;

    // Mark the question as answered (no one got it right)
    const newGameData = gameState === 'mainGameR1' ? [...generatedGameDataR1] : [...generatedGameDataR2];
    newGameData[questionToJudge.categoryIndex].questions[questionToJudge.questionIndex].answered = true;
    if (gameState === 'mainGameR1') {
      setGeneratedGameDataR1(newGameData);
    } else {
      setGeneratedGameDataR2(newGameData);
    }

    setMessage(`Player ${playerWhoPassed} passed. Player ${playerWhoPassed === 1 ? 2 : 1} can now buzz in.`);
    setUserAnswer(''); // Clear input for next player
    setBuzzedInPlayer(null); // Clear buzzer to allow other player to buzz in
    setShowAnswer(false); // Keep question open for second chance
    setIsSecondChance(true); // Indicate it's a second chance
    setOriginalBuzzer(playerWhoPassed); // Keep track of who passed first

    // If it's already a second chance and this player passes, then close the question
    if (isSecondChance) {
        setMessage('Both players passed. No one got it right.');
        setShowAnswer(true); // Show the answer
        // Turn goes to the player who *didn't* get the second chance
        setCurrentPlayer(originalBuzzer === 1 ? 2 : 1);
    }
  };

  // Function to get a hint using Gemini API
  const handleGetHint = async () => {
    setIsGeneratingHint(true);
    setGeneratedHint('');
    setShowHint(false); // Hide previous hint if any

    const questionSource = currentQuestion || dailyDoubleQuestionDetails;
    if (!questionSource) {
      setIsGeneratingHint(false);
      return;
    }

    const category = questionSource.category;
    const clue = questionSource.question;
    const answer = questionSource.answer; // Include answer for context, but instruct not to reveal

    try {
      const prompt = `Given the Jeopardy category "${category}", the clue "${clue}", and the correct answer "${answer}", provide a concise hint that helps someone guess the answer without directly giving it away. The hint should be a single sentence or a very short phrase.`;

      const chatHistory = [];
      chatHistory.push({ role: "user", parts: [{ text: prompt }] });

      const payload = {
        contents: chatHistory,
      };

      const apiKey = ""; // Canvas will automatically provide it in runtime
      const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (result.candidates && result.candidates.length > 0 &&
          result.candidates[0].content && result.candidates[0].content.parts &&
          result.candidates[0].content.parts.length > 0) {
        setGeneratedHint(result.candidates[0].content.parts[0].text);
        setShowHint(true);
      } else {
        console.error("Unexpected API response structure for hint:", result);
        setGeneratedHint('Could not generate a hint. Please try again.');
        setShowHint(true);
      }
    } catch (error) {
      console.error("Error generating hint:", error);
      setGeneratedHint(`Error generating hint: ${error.message}`);
      setShowHint(true);
    } finally {
      setIsGeneratingHint(false);
    }
  };


  // Function to close the question modal (main game & Daily Double)
  const closeQuestionModal = () => {
    setCurrentQuestion(null);
    setDailyDoubleQuestionDetails(null); // Clear DD specific details
    setMessage('');
    setUserAnswer('');
    setBuzzedInPlayer(null);
    setShowAnswer(false); // Reset show answer state
    setIsSecondChance(false); // Reset second chance
    setOriginalBuzzer(null); // Reset original buzzer
    setGeneratedHint(''); // Reset hint
    setShowHint(false); // Hide hint
    setIsGeneratingHint(false); // Reset hint loading state

    // Determine which round we are in to check for completion
    const currentRoundData = gameState.includes('mainGame') ? (gameState === 'mainGameR1' ? generatedGameDataR1 : generatedGameDataR2) : null;

    if (currentRoundData && checkAllQuestionsAnswered(currentRoundData)) {
      if (gameState === 'mainGameR1') {
        setGameState('categorySelectionR2'); // Move to Double Jeopardy category selection
      } else if (gameState === 'mainGameR2') {
        generateFinalJeopardyQuestion(); // Move to Final Jeopardy
      }
    } else if (gameState.includes('dailyDouble')) {
      // After a DD reveal, go back to the board of the current round
      setGameState(dailyDoubleQuestionDetails.round === 1 ? 'mainGameR1' : 'mainGameR2');
    }
  };

  // --- Daily Double Logic ---
  const submitDailyDoubleWager = () => {
    const wager = parseInt(dailyDoubleWagerAmount);
    const maxWager = currentPlayer === 1 ? player1Score : player2Score;

    // Max wager is either current score or the highest value on the board ($1000 for R1, $2000 for R2)
    const roundMaxQuestionValue = dailyDoubleQuestionDetails.round === 1 ? 1000 : 2000;
    const trueMaxWager = Math.max(maxWager, roundMaxQuestionValue);

    if (isNaN(wager) || wager < 5 || wager > trueMaxWager) { // Min wager $5
      setErrorGenerating(`Invalid wager. Must be between $5 and $${trueMaxWager} (your current score or max question value for this round).`);
      return;
    }
    setErrorGenerating('');
    setGameState('dailyDoubleQuestion');
  };

  // --- Final Jeopardy Logic ---

  // Submit wagers
  const submitWagers = () => {
    const p1Wager = parseInt(player1Wager);
    const p2Wager = parseInt(player2Wager);

    let wagerError = false;
    // Check for valid wagers
    if (isNaN(p1Wager) || p1Wager < 0 || p1Wager > player1Score) {
      setErrorGenerating('Player 1: Invalid wager. Must be a non-negative number not exceeding your score.');
      wagerError = true;
    }
    if (isNaN(p2Wager) || p2Wager < 0 || p2Wager > player2Score) {
      setErrorGenerating(prev => prev + (prev ? '\n' : '') + 'Player 2: Invalid wager. Must be a non-negative number not exceeding your score.');
      wagerError = true;
    }

    if (wagerError) return;

    setErrorGenerating('');
    setGameState('finalJeopardyQuestion');
  };

  // Submit final answers
  const submitFinalAnswers = () => {
    if (player1FinalAnswer.trim() === '' || player2FinalAnswer.trim() === '') {
      setErrorGenerating('Both players must type an answer before submitting.');
      return;
    }
    setErrorGenerating('');
    setGameState('finalJeopardyReveal');
  };

  // Judge individual final answer
  const judgeFinalAnswer = (player, isCorrect) => {
    if (player === 1) {
      const wager = parseInt(player1Wager);
      setPlayer1Score(prev => isCorrect ? prev + wager : prev - wager);
      setPlayer1FinalCorrect(isCorrect);
    } else {
      const wager = parseInt(player2Wager);
      setPlayer2Score(prev => isCorrect ? prev + wager : prev - wager);
      setPlayer2FinalCorrect(isCorrect);
    }
    setFinalAnswersRevealedCount(prev => prev + 1);
  };

  useEffect(() => {
    if (gameState === 'finalJeopardyReveal' && finalAnswersRevealedCount === 2) {
      // Both players have revealed their answers
      setTimeout(() => {
        setGameState('gameOver');
      }, 2000); // 2 second delay
    }
  }, [finalAnswersRevealedCount, gameState]);


  // Reset game function
  const resetGame = () => {
    setPlayer1Score(0);
    setPlayer2Score(0);
    setCurrentPlayer(1);
    setCurrentQuestion(null);
    setShowAnswer(false);
    setMessage('');
    setUserAnswer('');
    setBuzzedInPlayer(null);
    setGameState('categorySelectionR1'); // Go back to category selection for Round 1
    setSelectedCategoriesR1([]);
    setSelectedCategoriesR2([]);
    setGeneratedGameDataR1([]);
    setGeneratedGameDataR2([]);
    setNewCategoryInput('');
    setIsLoadingQuestions(false);
    setErrorGenerating('');
    // Reset Final Jeopardy states
    setFinalJeopardyCategory('');
    setFinalJeopardyClue('');
    setFinalJeopardyAnswer('');
    setPlayer1Wager('');
    setPlayer2Wager('');
    setPlayer1FinalAnswer('');
    setPlayer2FinalAnswer('');
    setPlayer1FinalCorrect(null);
    setPlayer2FinalCorrect(null);
    setFinalAnswersRevealedCount(0);
    // Reset Daily Double states
    setDailyDoubleQuestionDetails(null);
    setDailyDoubleWagerAmount('');
    // Reset Rebound states
    setIsSecondChance(false);
    setOriginalBuzzer(null);
    // Reset Hint states
    setGeneratedHint('');
    setShowHint(false);
    setIsGeneratingHint(false);
  };

  // Determine winner for Game Over screen
  const getWinner = () => {
    if (player1Score > player2Score) {
      return 'Player 1 wins!';
    } else if (player2Score > player1Score) {
      return 'Player 2 wins!';
    } else {
      return "It's a tie!";
    }
  };

  // Determine which game data to use for the current board display
  const currentBoardData = gameState === 'mainGameR1' ? generatedGameDataR1 : generatedGameDataR2;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-700 to-purple-800 text-white font-inter p-4 flex flex-col items-center justify-center">
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <script src="https://cdn.tailwindcss.com"></script>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet" />

      {/* Add custom CSS for the spin animation */}
      <style>
        {`
        @keyframes spinIn {
          from {
            transform: rotateY(90deg) scale(0.5);
            opacity: 0;
          }
          to {
            transform: rotateY(0deg) scale(1);
            opacity: 1;
          }
        }

        .spin-in {
          animation: spinIn 0.6s ease-out forwards;
        }
        `}
      </style>

      {/* Scoreboard - Always visible */}
      <div className="flex flex-col md:flex-row gap-4 mb-8 w-full justify-center">
        <div className={`bg-yellow-400 text-blue-900 font-bold text-2xl md:text-4xl p-3 md:p-5 rounded-xl shadow-lg border-4 flex items-center gap-2 ${currentPlayer === 1 && (gameState === 'mainGameR1' || gameState === 'mainGameR2') ? 'border-green-500' : 'border-yellow-200'}`}>
          PLAYER 1: $
          <input
            type="number"
            value={player1Score}
            onChange={(e) => setPlayer1Score(parseInt(e.target.value) || 0)}
            className="bg-transparent border-b-2 border-blue-900 w-24 text-blue-900 text-right font-bold text-2xl md:text-4xl focus:outline-none"
          />
        </div>
        <div className={`bg-yellow-400 text-blue-900 font-bold text-2xl md:text-4xl p-3 md:p-5 rounded-xl shadow-lg border-4 flex items-center gap-2 ${currentPlayer === 2 && (gameState === 'mainGameR1' || gameState === 'mainGameR2') ? 'border-green-500' : 'border-yellow-200'}`}>
          PLAYER 2: $
          <input
            type="number"
            value={player2Score}
            onChange={(e) => setPlayer2Score(parseInt(e.target.value) || 0)}
            className="bg-transparent border-b-2 border-blue-900 w-24 text-blue-900 text-right font-bold text-2xl md:text-4xl focus:outline-none"
          />
        </div>
      </div>

      {/* Conditional Rendering based on Game State */}

      {(gameState === 'categorySelectionR1' || gameState === 'categorySelectionR2') && (
        <div className="bg-blue-900 p-8 rounded-xl shadow-2xl max-w-xl w-full border-4 border-yellow-400">
          <h2 className="text-3xl md:text-4xl font-bold text-yellow-400 mb-6 text-center">
            Choose Categories for {gameState === 'categorySelectionR1' ? 'Round 1 (Single Jeopardy)' : 'Round 2 (Double Jeopardy)'}
          </h2>
          <div className="flex flex-col sm:flex-row gap-2 mb-4">
            <input
              type="text"
              value={newCategoryInput}
              onChange={(e) => setNewCategoryInput(e.target.value)}
              placeholder="Enter category name..."
              className="flex-1 p-3 rounded-lg bg-blue-800 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  addCategory();
                }
              }}
            />
            <button
              onClick={addCategory}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl shadow-md transition-transform transform hover:scale-105 active:scale-100 border-2 border-green-500"
            >
              Add Category
            </button>
          </div>

          {(gameState === 'categorySelectionR1' ? selectedCategoriesR1 : selectedCategoriesR2).length > 0 && (
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-yellow-300 mb-2">Selected Categories:</h3>
              <div className="flex flex-wrap gap-2">
                {(gameState === 'categorySelectionR1' ? selectedCategoriesR1 : selectedCategoriesR2).map((cat, index) => (
                  <span key={index} className="bg-blue-700 text-white px-3 py-1 rounded-full flex items-center gap-2">
                    {cat}
                    <button onClick={() => removeCategory(cat)} className="text-red-300 hover:text-red-500 font-bold text-lg leading-none">
                      &times;
                    </button>
                  </span>
                ))}
              </div>
            </div>
          )}

          {errorGenerating && (
            <p className="text-red-400 text-center mb-4">{errorGenerating}</p>
          )}

          <button
            onClick={() => handleStartRound(gameState === 'categorySelectionR1' ? 1 : 2)}
            className="w-full px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-purple-500"
            disabled={isLoadingQuestions || (gameState === 'categorySelectionR1' ? selectedCategoriesR1.length === 0 : selectedCategoriesR2.length === 0)}
          >
            {isLoadingQuestions ? 'Generating Questions...' : `Start ${gameState === 'categorySelectionR1' ? 'Round 1' : 'Round 2'}`}
          </button>
          {isLoadingQuestions && (
            <p className="text-center text-yellow-300 mt-4">This might take a moment...</p>
          )}
        </div>
      )}

      {(gameState === 'mainGameR1' || gameState === 'mainGameR2') && (
        <>
          <h3 className="text-xl md:text-3xl font-bold text-yellow-300 mb-6">
            Player to choose next question: Player {currentPlayer}
          </h3>
          <h3 className="text-xl md:text-3xl font-bold text-yellow-300 mb-6">
            Round: {gameState === 'mainGameR1' ? 'Single Jeopardy' : 'Double Jeopardy'}
          </h3>

          {/* Game Board */}
          <div className="w-full max-w-6xl overflow-x-auto">
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 md:gap-4 p-2 md:p-4 bg-blue-900 rounded-xl shadow-2xl border-4 border-blue-700">
              {currentBoardData.map((category, catIndex) => (
                <div key={catIndex} className="flex flex-col">
                  {/* Category Header */}
                  <div className="bg-blue-600 text-white font-bold text-sm md:text-xl p-2 md:p-4 rounded-t-lg border-b-2 border-blue-500 text-center uppercase shadow-md">
                    {category.category}
                  </div>
                  {/* Questions */}
                  {category.questions.map((q, qIndex) => (
                    <button
                      key={qIndex}
                      className={`
                        flex items-center justify-center
                        h-16 md:h-24
                        bg-blue-800 text-yellow-400 font-bold text-xl md:text-3xl
                        rounded-b-lg md:rounded-lg
                        border-2 border-blue-700
                        transition-all duration-200 ease-in-out
                        ${q.answered ? 'opacity-50 cursor-not-allowed bg-blue-950 text-gray-500' : 'hover:bg-blue-700 hover:scale-105 active:bg-blue-600 active:scale-100'}
                        ${qIndex === category.questions.length - 1 ? 'rounded-b-lg' : 'rounded-none'}
                        ${qIndex === 0 ? 'rounded-t-none' : ''}
                      `}
                      onClick={() => handleCellClick(catIndex, qIndex)}
                      disabled={q.answered}
                    >
                      {q.answered ? '' : `$${q.value}`}
                    </button>
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Reset Button */}
          <button
            onClick={resetGame}
            className="mt-8 px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-red-500"
          >
            Reset Game
          </button>

          {/* Question Modal (Main Game) */}
          {currentQuestion && (
            <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
              <div className="bg-blue-800 text-white p-6 md:p-8 rounded-xl shadow-2xl max-w-2xl w-full border-4 border-yellow-400 relative spin-in"> {/* Added spin-in class */}
                <h2 className="text-2xl md:text-4xl font-bold text-yellow-400 mb-4 text-center">
                  ${currentQuestion.value} - {currentBoardData[currentQuestion.categoryIndex].category}
                </h2>
                <p className="text-lg md:text-2xl mb-6 text-center">
                  {currentQuestion.question}
                </p>

                {message && (
                  <p className={`text-center text-xl md:text-3xl font-bold mb-4 ${message === 'Correct!' ? 'text-green-400' : 'text-red-400'}`}>
                    {message}
                  </p>
                )}

                {/* Buzzer Buttons - visible until someone buzzes in or answer is shown */}
                {!buzzedInPlayer && !showAnswer && (
                  <div className="flex flex-col sm:flex-row justify-center gap-4 mb-6">
                    <button
                      onClick={() => handleBuzzIn(1)}
                      className="flex-1 px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-purple-500"
                      disabled={isSecondChance && originalBuzzer === 1} // Disable if P1 buzzed first and it's second chance
                    >
                      Player 1 Buzz In!
                    </button>
                    <button
                      onClick={() => handleBuzzIn(2)}
                      className="flex-1 px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-purple-500"
                      disabled={isSecondChance && originalBuzzer === 2} // Disable if P2 buzzed first and it's second chance
                    >
                      Player 2 Buzz In!
                    </button>
                  </div>
                )}

                {/* Input and Submit/Reveal Buttons - visible only after a player buzzes in and before answer is shown */}
                {buzzedInPlayer && !showAnswer && (
                  <div className="flex flex-col gap-4 mb-6">
                    <p className="text-center text-xl md:text-2xl font-semibold text-yellow-300">Player {buzzedInPlayer}'s turn to answer!</p>
                    <input
                      type="text"
                      value={userAnswer}
                      onChange={(e) => setUserAnswer(e.target.value)}
                      placeholder="Type your answer here..."
                      className="p-3 rounded-lg bg-blue-900 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          checkAnswer();
                        }
                      }}
                    />
                    <div className="flex flex-col sm:flex-row justify-center gap-4">
                      <button
                        onClick={checkAnswer}
                        className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-green-500"
                      >
                        Submit Answer
                      </button>
                      <button
                        onClick={revealAnswer}
                        className="flex-1 px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-red-500"
                      >
                        Reveal Answer
                      </button>
                      <button
                        onClick={handlePass} // New Pass button
                        className="flex-1 px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-gray-500"
                      >
                        Pass
                      </button>
                    </div>
                    <button
                      onClick={handleGetHint}
                      className="w-full mt-4 px-6 py-3 bg-yellow-600 hover:bg-yellow-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-yellow-500"
                      disabled={isGeneratingHint}
                    >
                      {isGeneratingHint ? 'Generating Hint...' : 'Get a Hint'}
                    </button>
                    {showHint && generatedHint && (
                      <div className="mt-4 p-4 bg-blue-900 rounded-lg border border-blue-700">
                        <h3 className="text-lg md:text-xl font-semibold text-yellow-300 mb-2">Hint:</h3>
                        <p className="text-md md:text-lg">{generatedHint}</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Correct Answer Display - visible after answer is judged or revealed */}
                {showAnswer && (
                  <div className="mt-4 p-4 bg-blue-900 rounded-lg border border-blue-700">
                    <h3 className="text-lg md:text-xl font-semibold text-yellow-300 mb-2">The correct response is:</h3>
                    <p className="text-xl md:text-3xl font-bold">{currentQuestion.answer}</p>
                  </div>
                )}

                {/* Close Button - visible only after answer is shown */}
                {showAnswer && (
                  <div className="flex justify-center mt-8">
                    <button
                      onClick={closeQuestionModal}
                      className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-blue-500"
                    >
                      Close
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {/* Daily Double Wager Modal */}
      {gameState === 'dailyDoubleWager' && dailyDoubleQuestionDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-blue-800 text-white p-6 md:p-8 rounded-xl shadow-2xl max-w-2xl w-full border-4 border-yellow-400 relative spin-in"> {/* Added spin-in class */}
            <h2 className="text-3xl md:text-4xl font-bold text-yellow-400 mb-4 text-center">DAILY DOUBLE!</h2>
            <p className="text-xl md:text-2xl mb-4 text-center">Category: <span className="font-bold">{dailyDoubleQuestionDetails.category}</span></p>
            <p className="text-lg md:text-xl mb-6 text-center">Player {currentPlayer}, enter your wager:</p>
            <p className="text-lg md:text-xl mb-4 text-center text-yellow-300">Your current score: ${currentPlayer === 1 ? player1Score : player2Score}</p>

            {errorGenerating && (
              <p className="text-red-400 text-center mb-4">{errorGenerating}</p>
            )}

            <input
              type="number"
              value={dailyDoubleWagerAmount}
              onChange={(e) => setDailyDoubleWagerAmount(e.target.value)}
              placeholder="Enter wager..."
              className="w-full p-3 rounded-lg bg-blue-900 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400 mb-6"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  submitDailyDoubleWager();
                }
              }}
            />
            <button
              onClick={submitDailyDoubleWager}
              className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-green-500"
            >
              Submit Wager
            </button>
          </div>
        </div>
      )}

      {/* Daily Double Question Modal */}
      {gameState === 'dailyDoubleQuestion' && dailyDoubleQuestionDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-blue-800 text-white p-6 md:p-8 rounded-xl shadow-2xl max-w-2xl w-full border-4 border-yellow-400 relative spin-in"> {/* Added spin-in class */}
            <h2 className="text-3xl md:text-4xl font-bold text-yellow-400 mb-4 text-center">DAILY DOUBLE!</h2>
            <p className="text-xl md:text-2xl mb-4 text-center">Category: <span className="font-bold">{dailyDoubleQuestionDetails.category}</span></p>
            <p className="text-lg md:text-2xl mb-6 text-center">Clue: <span className="font-semibold">{dailyDoubleQuestionDetails.question}</span></p>
            <p className="text-lg md:text-xl mb-6 text-center text-yellow-300">Wager: ${dailyDoubleWagerAmount}</p>

            {message && (
              <p className={`text-center text-xl md:text-3xl font-bold mb-4 ${message === 'Correct!' ? 'text-green-400' : 'text-red-400'}`}>
                {message}
              </p>
            )}

            {!showAnswer && (
              <div className="flex flex-col gap-4 mb-6">
                <p className="text-center text-xl md:text-2xl font-semibold text-yellow-300">Player {currentPlayer}'s turn to answer!</p>
                <input
                  type="text"
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Type your answer here..."
                  className="p-3 rounded-lg bg-blue-900 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      checkAnswer();
                    }
                  }}
                />
                <div className="flex flex-col sm:flex-row justify-center gap-4">
                  <button
                    onClick={checkAnswer}
                    className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-green-500"
                  >
                    Submit Answer
                  </button>
                  <button
                    onClick={revealAnswer}
                    className="flex-1 px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-red-500"
                  >
                    Reveal Answer
                  </button>
                </div>
                <button
                  onClick={handleGetHint}
                  className="w-full mt-4 px-6 py-3 bg-yellow-600 hover:bg-yellow-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-yellow-500"
                  disabled={isGeneratingHint}
                >
                  {isGeneratingHint ? 'Generating Hint...' : 'Get a Hint'}
                </button>
                {showHint && generatedHint && (
                  <div className="mt-4 p-4 bg-blue-900 rounded-lg border border-blue-700">
                    <h3 className="text-lg md:text-xl font-semibold text-yellow-300 mb-2">Hint:</h3>
                    <p className="text-md md:text-lg">{generatedHint}</p>
                  </div>
                )}
              </div>
            )}

            {showAnswer && (
              <div className="mt-4 p-4 bg-blue-900 rounded-lg border border-blue-700">
                <h3 className="text-lg md:text-xl font-semibold text-yellow-300 mb-2">The correct response is:</h3>
                <p className="text-xl md:text-3xl font-bold">{dailyDoubleQuestionDetails.answer}</p>
              </div>
            )}

            {showAnswer && (
              <div className="flex justify-center mt-8">
                <button
                  onClick={closeQuestionModal}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-blue-500"
                >
                  Close
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Final Jeopardy Wager Modal */}
      {gameState === 'finalJeopardyWager' && (
        <div className="bg-blue-900 p-8 rounded-xl shadow-2xl max-w-xl w-full border-4 border-yellow-400">
          <h2 className="text-3xl md:text-4xl font-bold text-yellow-400 mb-6 text-center">Final Jeopardy!</h2>
          <p className="text-xl md:text-2xl mb-4 text-center">Category: <span className="font-bold">{finalJeopardyCategory}</span></p>
          <p className="text-lg md:text-xl mb-6 text-center">Enter your wager (cannot exceed your current score):</p>

          {errorGenerating && (
            <p className="text-red-400 text-center mb-4">{errorGenerating}</p>
          )}

          <div className="flex flex-col gap-4 mb-6">
            <div className="flex flex-col">
              <label htmlFor="player1Wager" className="text-yellow-300 mb-1">Player 1 Wager (Current Score: ${player1Score}):</label>
              <input
                id="player1Wager"
                type="number"
                value={player1Wager}
                onChange={(e) => setPlayer1Wager(e.target.value)}
                min="0"
                max={player1Score}
                className="p-3 rounded-lg bg-blue-800 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              />
            </div>
            <div className="flex flex-col">
              <label htmlFor="player2Wager" className="text-yellow-300 mb-1">Player 2 Wager (Current Score: ${player2Score}):</label>
              <input
                id="player2Wager"
                type="number"
                value={player2Wager}
                onChange={(e) => setPlayer2Wager(e.target.value)}
                min="0"
                max={player2Score}
                className="p-3 rounded-lg bg-blue-800 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              />
            </div>
          </div>
          <button
            onClick={submitWagers}
            className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-green-500"
          >
            Submit Wagers
          </button>
        </div>
      )}

      {gameState === 'finalJeopardyQuestion' && (
        <div className="bg-blue-900 p-8 rounded-xl shadow-2xl max-w-xl w-full border-4 border-yellow-400">
          <h2 className="text-3xl md:text-4xl font-bold text-yellow-400 mb-6 text-center">Final Jeopardy!</h2>
          <p className="text-xl md:text-2xl mb-4 text-center">Category: <span className="font-bold">{finalJeopardyCategory}</span></p>
          <p className="text-lg md:text-2xl mb-6 text-center">Clue: <span className="font-semibold">{finalJeopardyClue}</span></p>

          {errorGenerating && (
            <p className="text-red-400 text-center mb-4">{errorGenerating}</p>
          )}

          <div className="flex flex-col gap-4 mb-6">
            <div className="flex flex-col">
              <label htmlFor="player1FinalAnswer" className="text-yellow-300 mb-1">Player 1 Answer:</label>
              <input
                id="player1FinalAnswer"
                type="text"
                value={player1FinalAnswer}
                onChange={(e) => setPlayer1FinalAnswer(e.target.value)}
                placeholder="Type your answer here..."
                className="p-3 rounded-lg bg-blue-800 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              />
            </div>
            <div className="flex flex-col">
              <label htmlFor="player2FinalAnswer" className="text-yellow-300 mb-1">Player 2 Answer:</label>
              <input
                id="player2FinalAnswer"
                type="text"
                value={player2FinalAnswer}
                onChange={(e) => setPlayer2FinalAnswer(e.target.value)}
                placeholder="Type your answer here..."
                className="p-3 rounded-lg bg-blue-800 text-white border border-blue-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              />
            </div>
          </div>
          <button
            onClick={submitFinalAnswers}
            className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-green-500"
          >
            Submit Final Answers
          </button>
        </div>
      )}

      {gameState === 'finalJeopardyReveal' && (
        <div className="bg-blue-900 p-8 rounded-xl shadow-2xl max-w-xl w-full border-4 border-yellow-400">
          <h2 className="text-3xl md:text-4xl font-bold text-yellow-400 mb-6 text-center">Final Jeopardy Reveal!</h2>
          <p className="text-xl md:text-2xl mb-4 text-center">Category: <span className="font-bold">{finalJeopardyCategory}</span></p>
          <p className="text-lg md:text-2xl mb-6 text-center">Clue: <span className="font-semibold">{finalJeopardyClue}</span></p>
          <p className="text-xl md:text-2xl mb-6 text-center font-bold text-yellow-300">Correct Response: {finalJeopardyAnswer}</p>

          <div className="flex flex-col gap-6">
            {/* Player 1 Reveal */}
            <div className="bg-blue-800 p-4 rounded-lg border border-blue-700">
              <h3 className="text-xl font-semibold text-yellow-300 mb-2">Player 1's Answer:</h3>
              <p className="text-lg mb-4">{player1FinalAnswer}</p>
              {player1FinalCorrect === null ? (
                <div className="flex gap-2 justify-center">
                  <button
                    onClick={() => judgeFinalAnswer(1, true)}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg shadow-md"
                  >
                    Player 1 Correct
                  </button>
                  <button
                    onClick={() => judgeFinalAnswer(1, false)}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg shadow-md"
                  >
                    Player 1 Incorrect
                  </button>
                </div>
              ) : (
                <p className={`text-center font-bold ${player1FinalCorrect ? 'text-green-400' : 'text-red-400'}`}>
                  Player 1: {player1FinalCorrect ? 'Correct!' : 'Incorrect!'}
                </p>
              )}
            </div>

            {/* Player 2 Reveal */}
            <div className="bg-blue-800 p-4 rounded-lg border border-blue-700">
              <h3 className="text-xl font-semibold text-yellow-300 mb-2">Player 2's Answer:</h3>
              <p className="text-lg mb-4">{player2FinalAnswer}</p>
              {player2FinalCorrect === null ? (
                <div className="flex gap-2 justify-center">
                  <button
                    onClick={() => judgeFinalAnswer(2, true)}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg shadow-md"
                  >
                    Player 2 Correct
                  </button>
                  <button
                    onClick={() => judgeFinalAnswer(2, false)}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg shadow-md"
                  >
                    Player 2 Incorrect
                  </button>
                </div>
              ) : (
                <p className={`text-center font-bold ${player2FinalCorrect ? 'text-green-400' : 'text-red-400'}`}>
                  Player 2: {player2FinalCorrect ? 'Correct!' : 'Incorrect!'}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {gameState === 'gameOver' && (
        <div className="bg-blue-900 p-8 rounded-xl shadow-2xl max-w-xl w-full border-4 border-yellow-400 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-yellow-400 mb-6">Game Over!</h2>
          <p className="text-2xl md:text-3xl text-white mb-4">Final Scores:</p>
          <p className="text-xl md:text-2xl text-yellow-300 mb-2">Player 1: ${player1Score}</p>
          <p className="text-xl md:text-2xl text-yellow-300 mb-6">Player 2: ${player2Score}</p>
          <h3 className="text-3xl md:text-4xl font-bold text-green-400 mb-8">{getWinner()}</h3>
          <button
            onClick={resetGame}
            className="px-8 py-4 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-lg transition-transform transform hover:scale-105 active:scale-100 border-2 border-red-500"
          >
            Play Again
          </button>
        </div>
      )}
    </div>
  );
};

export default App;