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
            <div ref="expPanel"></div>
            <v-expansion-panels>
              <v-expansion-panel
                v-if="isSelected"
                :title="selectedGroup"
              >
              <v-progress-linear
                indeterminate
                color="primary"
                :height="10"
                v-if="isLoading"
              ></v-progress-linear>
                <h3>ЧИСЛИТЕЛЬ</h3>
                <template
                  v-for="week, shcId in allScheduleByGroupChislitel"
                  :key="shcId"
                >
                  ДЕНЬ НЕДЕЛИ
                  <template
                    v-for="day, group in week"
                    :key="group"
                  >
                    <template
                      v-for="d, id in day"
                      :key="id"
                    >
                      <div v-if="d == ''">
                        Нет пары
                      </div>
                      <div>
                        {{ d }}
                      </div>
                    </template>
                    <v-divider :thickness="10"></v-divider>
                  </template>
                </template>

                <h3>ЗНАМЕНАТЕЛЬ</h3>

                <template
                  v-for="week, shcId in allScheduleByGroupChislitel"
                  :key="shcId"
                >
                  ДЕНЬ НЕДЕЛИ
                  <template
                    v-for="day, group in week"
                    :key="group"
                  >
                    <template
                      v-for="d, id in day"
                      :key="id"
                    >
                      <div v-if="d == ''">
                        Нет пары
                      </div>
                      <div>
                        {{ d }}
                      </div>
                    </template>
                    <v-divider :thickness="10"></v-divider>
                  </template>
                </template>
              </v-expansion-panel>
            </v-expansion-panels>

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
const isLoading = ref(false);
let allScheduleByGroupChislitel = ref();
let allScheduleByGroupZnamenatel = ref()

const expPanel = ref()

class ScheduleApi {
  apiUrl = 'https://router-mocha.vercel.app/';
  getGroupsUrl = 'getGroups';
  getAllScheduleByGroupUrl = 'getAllScheduleByGroup';

  async getGroups() {
    let result = await axios.get(this.apiUrl + this.getGroupsUrl)
    groups.value = result.data
  }
  async getAllScheduleByGroup<T>(group: T) {
    let result: allSchedule = await axios.get(this.apiUrl + this.getAllScheduleByGroupUrl, {
      params: { 'group': group }
    })
    allScheduleByGroupChislitel.value = result.data?.chislit
    allScheduleByGroupZnamenatel.value = result.data?.znamenat
  }
}
type allSchedule = {
  'data'?: {
    'chislit': {
      '0': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '1': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '2': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '3': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '4': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '5': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
    },
    'znamenat': {
      '0': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '1': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '2': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '3': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '4': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
      '5': {
        'group': {
          '0': ''
          '1': ''
          '2': ''
          '3': ''
          '4': ''
          '5': ''
        }
      }
    }
  }
}
const scheduleApi = new ScheduleApi()

function toggleSelected<T>(group: T) {
  isLoading.value = true

  if (selectedGroup.value == group) {
    selectedGroup.value = null;
    isSelected.value = false;
    return false;
  }

  selectedGroup.value = group;
  scheduleApi.getAllScheduleByGroup(group);
  isSelected.value = true;
  expPanel.value.scrollIntoView({ behavior: "smooth" });
  setTimeout(()=>{
    isLoading.value = false
  },500)
}

onBeforeMount(() => {
  scheduleApi.getGroups();
})
</script>
