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

        <groups-chips />

        <div
          class="mt-10"
          ref="anchor"
        >
        </div>

        <schedule-list v-if="isSelected" />

      </v-col>

    </v-row>


  </v-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAppStore } from '@/store/app';
import { storeToRefs } from 'pinia';
import GroupsChips from './GroupsChips.vue';
import ScheduleList from './ScheduleList.vue';

const store = useAppStore()
const { isGroupsLoading, isSelected, anchor } = storeToRefs(store)

</script>



<style>
body {
  height: 150vh;
}
</style>