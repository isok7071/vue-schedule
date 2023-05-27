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
            <div
              v-for="id, group in groups"
              :key="id"
            >
              <v-expansion-panels>
                <v-chip
                  filter
                  @group:selected="toggleSelected(group)"
                >
                  {{ group }}
                </v-chip>
                <v-expansion-panel
                  v-if="isSelected == group"
                  title="Title"
                >
                <div 
                  v-for="para, shcId in allScheduleByGroup"
                  :key="shcId"
                >
                {{ para }}
              </div>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>

          </v-chip-group>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
let groups = ref([]);
let selectedGroup = ref();
let isSelected = ref();
let allScheduleByGroup = ref();

class ScheduleApi{
  apiUrl = 'https://router-mocha.vercel.app/';
  getGroupsUrl = 'getGroups';
  getAllScheduleByGroupUrl = 'getAllScheduleByGroup';

  async getGroups() {
  let result = await axios.get(this.apiUrl+this.getGroupsUrl)
  groups.value = result.data
}
async getAllScheduleByGroup<T>(group: T) {
  let result = await axios.get(this.apiUrl+this.getAllScheduleByGroupUrl,{
    params: {'group':group}
  })
  allScheduleByGroup.value = result.data.chislit.friday[group]
}
}

const scheduleApi = new ScheduleApi()

function toggleSelected<T>(group: T) {
  if (selectedGroup.value == group) {
    selectedGroup.value = null;
    isSelected.value = false;
    return false;
  }
  scheduleApi.getAllScheduleByGroup(group);

  selectedGroup.value = group;
  isSelected.value = group;
}

onBeforeMount(() => {
  scheduleApi.getGroups();
})
</script>
