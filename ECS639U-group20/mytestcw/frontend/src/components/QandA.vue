<template>
  <!-- npm run dev -->
  <div v-if="item.user!=user_id">
    <div class="input-group p-2 ">
      <input class="form-control" type="text" id="question" name="question" placeholder="Ask a question" />
      <button class="btn btn-success" @click="askQuestion(user_id!,item_id!)">Ask</button>
    </div>
  </div>

  <hr/>
  <div v-for="eachQuestion in questions">
    <table class="table">
      <tr>
          <td class = "fw-bold fs-5 align-bottom col-sm-1">Q</td>
          <td class = "text-start fs-5 align-bottom text-primary">{{ eachQuestion.question_body }}</td>
      </tr>
      <tr>
          <td class = "col-sm-1"></td>
          <td class = "text-start text-secondary align-top"><small class="p-0"> - from {{eachQuestion.user}} at {{formatDate(eachQuestion.question_time)}}</small></td>
      </tr>
      </table>

    <div v-if="eachQuestion.answer">
      <table class="table">
      <tr>
          <td class = "fw-bold fs-5 align-bottom col-sm-1 ">A</td>
          <td class = "text-start fs-5 align-bottom">{{eachQuestion.answer}}</td>
      </tr>
      <tr>
          <td class = "col-sm-1"></td>
          <td class = "text-start text-secondary" colspan="2"><small class="p-0"> - from seller</small></td>
      </tr>
      </table>
    </div>
    <div v-else v-if="item.user===user_id" class="row mx-5">
      <button class="btn btn-light px-0" @click="getQuestion(eachQuestion.id); allowAnswer = true;">Reply</button>
    </div>

    <div v-if="question.id == eachQuestion.id">
      <div v-show="allowAnswer" class="row m-5">
        <input class="col-9 col-sm-8 rounded-start border border-1" type="text" id="answer" name="answer" :placeholder="'Reply '+eachQuestion.user"/>
        <button class="col col-sm-2 btn btn-success rounded-0" @click="answerQuestion(2,eachQuestion.id)">Reply</button>
        <button class="col col-sm-2 btn btn-secondary rounded-0 rounded-end" @click="allowAnswer = false">Cancel</button>
      </div>
    </div>

    <hr/>
  </div>
</template>
  
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  data(){
    return{
      questions: [] as {id: number, question_body: string, question_time: string, answer: string, item: string, user: string}[],
      question: [] as any,
      //question: [] as {id: number, question_body: string, question_time: string, answer: string, item: string, user: string}[],
      allowAnswer: false,
      item: [] as any,
    };
  },
  props: {
      user_id: Number,
      item_id: Number,
  },
  mounted() {
    this.getQuestions()
    this.getItem()
  },
  methods: {
    formatDate(submitDate: string) {
      const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

      var date = new Date(submitDate)

      let day = date.getDate()
      let month = monthNames[date.getMonth()]
      let year = date.getFullYear()
      var strDate = day + " " + month + " " + year

      var hours = date.getHours();
      var minutes: string |number;
      minutes = date.getMinutes();
      var ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12;
      hours = hours ? hours : 12; // the hour '0' should be '12'
      minutes = minutes < 10 ? '0' + minutes : minutes;
      var strTime = hours + ':' + minutes + ' ' + ampm;
      return (strDate + "  " + strTime);
    },
    async getQuestions(){
      let response = await fetch("/api/questions/");
      let data = await response.json();
      this.questions = data.questions;
      console.log(data);
      console.log(this.item_id)
      var filterResult = this.questions.filter((x) => { 
        return x.item == String(this.item_id); 
      });
      console.log("questions should be here:"+filterResult);
      this.questions = filterResult
      // console.log("Merge:"+this.questions[2].id)
    },
    async getQuestion(question_id: number){
      let response = await fetch("/api/question/" + question_id);
      let data = await response.json();
      this.question = data;

      console.log(data);
      console.log(this.question);
    },
    async askQuestion(user_id: number, item_id: number){
      let new_question = (<HTMLInputElement>document.getElementById("question")).value;
      let now = new Date();
      let new_entry = {
        question_body: new_question,
        question_time: now,
        item: item_id,
        user: user_id
      }
      let response = await fetch("/api/questions/", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(new_entry)
      });
      if(response.ok){
        this.getQuestions();
        (<HTMLInputElement>document.getElementById("question")).value = ""
      }
      else
        alert("Question cannot be submitted. Try again later");
    },
    async answerQuestion(user_id: number, question_id: number){
      let owner_answer = (<HTMLInputElement>document.getElementById("answer")).value;
      let now = new Date();
      let new_entry= {
        answer_body: owner_answer,
        answer_time: now,
        user: user_id,
        question: question_id,
      }

      let response = await fetch("/api/answers/", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(new_entry)
      });
      if(response.ok){
        this.getQuestions();
        this.allowAnswer= false;
      }
      else
        alert("Question cannot be submitted. Try again later");
    },
    async getItem(){
      console.log(this.item_id)
      let response = await fetch("/api/item/" +this.item_id);
      let data = await response.json();
      this.item = data;
      console.log("Item belongs to:" +this.item.user)
    },
  }
})
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup

</script>
  
<style>
</style>