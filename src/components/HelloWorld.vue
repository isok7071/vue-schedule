<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
    
      <v-row class="d-flex align-center justify-center">
        <v-col cols="auto">
          <h1>Hello</h1>
          <v-chip-group
            selected-class="text-primary"
            column
          >
          
            <v-chip
              v-for="id,group in groups"
              :key="id"
            >
              {{ group }}
            </v-chip>
          </v-chip-group>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
import {onMounted, ref } from 'vue';
import axios from 'axios';

let groups = ref([]);

async function getGroups(){
    const groupsUrl = 'https://petrovsky-bot.ru:12100/getGroups'
    let result = await axios.get(groupsUrl)
    groups.value = result.data
  }


onMounted( ()=>{
  getGroups();

// fetch('http://petrovsky-bot.ru:12100/getByGroup')
// .then(response => response.json())
// .then(data => console.log(data));


})
</script>
