<template>
  <v-container class="fill-height">
      <v-row class="d-flex align-center justify-center">
        <v-col cols="auto">
        <v-container class="text-center">
          <h1>Расписание по группе</h1>

          <v-progress-circular
            indeterminate
            color="primary"
            v-if="isGroupsLoading"
            :size="100"
            :width="10"
            
          ></v-progress-circular>
        </v-container>
          <v-chip-group
            selected-class="text-primary"
            column
          >
            <template
              v-for="id, group in groups"
              :key="id"
            >

              <v-chip
                filter
                @group:selected="toggleSelected(group)"
              >
                {{ group }}
              </v-chip>
            </template>



            <v-progress-linear
              indeterminate
              color="primary"
              :height="10"
              v-if="isLoading"
            ></v-progress-linear>
          </v-chip-group>
          <div
            class="mt-10"
            ref="anchor"
          >
          </div>
          <template v-if="isSelected">
            <v-row>
              <template
                v-for="schedule, shcId in allScheduleByGroup"
                :key="shcId"
              >
                <v-col>
                  <v-card
                    v-for="dayId, day in schedule"
                    :key="dayId"
                    height="100%"
                    class="pt-4 rounded-lg"
                  >
                    <v-card-title class="text-primary">{{ day }}</v-card-title>
                    <template
                      v-for="groupRasp, group in dayId"
                      :key="group"
                    >
                      <ol>
                        <template
                          v-for="para, paraId in groupRasp"
                          :key="paraId"
                        >
                          <v-card-text
                            class="ml-3"
                            v-if="para == ''"
                          >
                            <li> Нет пары</li>
                          </v-card-text>
                          <v-card-text
                            class="ml-3"
                            v-else
                          >
                            <li>{{ para }}</li>
                          </v-card-text>
                          <v-divider
                            :thickness="2"
                            color="primary"
                          ></v-divider>
                        </template>
                      </ol>

                    </template>

                  </v-card>
                </v-col>
              </template>
            </v-row>

          </template>

        </v-col>

      </v-row>


  </v-container>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
let groups = ref([]);
let selectedGroup = ref();
let isSelected = ref();
const isLoading = ref(false);
const isGroupsLoading = ref(true);

let allScheduleByGroup = ref();

const anchor = ref()

class ScheduleApi {
  apiUrl = 'https://bot.imsokserver70.keenetic.link/';
  getGroupsUrl = 'getGroups';
  getAllScheduleByGroupUrl = 'getByGroup';

  async getGroups() {
    let result = await axios.get(this.apiUrl + this.getGroupsUrl)
    isGroupsLoading.value = false;
    groups.value = result.data
  }
  async getAllScheduleByGroup<T>(group: T) {
    let result: allSchedule = await axios.get(this.apiUrl + this.getAllScheduleByGroupUrl, {
      params: { 'group': group }
    })
    allScheduleByGroup.value = result.data
  }
}
type allSchedule = {
  'data'?: {
    '0': {
      'today': {
        'group': {
          '0': '',
          '1': '',
          '2': '',
          '3': '',
          '4': '',
          '5': '',
          '6': '',
        },
      },
    },
    '1': {
      'next_day': {
        'group': {
          '0': '',
          '1': '',
          '2': '',
          '3': '',
          '4': '',
          '5': '',
          '6': '',
        },
      },

    }
  }
}
const scheduleApi = new ScheduleApi()

function toggleSelected<T>(group: T) {
  isLoading.value = true

  if (selectedGroup.value == group) {
    selectedGroup.value = '';
    isSelected.value = false;
    isLoading.value = false
    return false;
  }
  selectedGroup.value = '';
  allScheduleByGroup.value = {}
  selectedGroup.value = group;
  scheduleApi.getAllScheduleByGroup(group);
  isSelected.value = true;
  anchor.value.scrollIntoView({ behavior: "smooth" });
  setTimeout(() => {
    isLoading.value = false
  }, 500)
}

onBeforeMount(() => {
  scheduleApi.getGroups();
})
</script>

<style>
body {
  height: 150vh;
}
</style>