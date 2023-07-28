import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAppStore = defineStore('app', () => {

  const apiUrl = 'https://bot.imsokserver70.keenetic.link/';
  const getGroupsUrl = 'getGroups';
  const getAllScheduleByGroupUrl = 'getByGroup';

  const groups = ref([]);
  const isGroupsLoading = ref(true);
  const allScheduleByGroup = ref();
  const isLoading = ref(false);
  const isSelected = ref();
  const selectedGroup = ref();

  //Якорь до которого работает скроллинг
  const anchor = ref()


  async function getGroups() {
    const result = await axios.get(apiUrl + getGroupsUrl)
    isGroupsLoading.value = false;
    groups.value = result.data
  }

  async function getAllScheduleByGroup<T>(group: T) {
    const result: allSchedule = await axios.get(apiUrl + getAllScheduleByGroupUrl, {
      params: { 'group': group }
    })
    allScheduleByGroup.value = result.data
  }


  function toggleSelected<T>(group: T) {
    isLoading.value = true

    if (selectedGroup.value === group) {
      selectedGroup.value = '';
      isSelected.value = false;
      isLoading.value = false
      return false;
    }

    allScheduleByGroup.value = {}
    selectedGroup.value = group;
    getAllScheduleByGroup(group);

    isSelected.value = true;

    anchor.value.scrollIntoView({ behavior: "smooth" });
    setTimeout(() => {
      isLoading.value = false
    }, 500)
  }

  return { anchor, getGroups, getAllScheduleByGroup, groups, isGroupsLoading, allScheduleByGroup, isLoading, toggleSelected, isSelected, selectedGroup }
})
