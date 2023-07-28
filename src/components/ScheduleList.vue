<template>
    <v-row>
        <template
            v-for="schedule, shcId in allScheduleByGroup"
            :key="shcId"
        >
            <schedule-item :schedule="schedule"/>
        </template>
    </v-row>
</template>

<script lang="ts" setup>
import { useAppStore } from '@/store/app';
import { storeToRefs } from 'pinia';
import ScheduleItem from './ScheduleItem.vue';

const store = useAppStore()
const { allScheduleByGroup, selectedGroup } = storeToRefs(store)

store.getAllScheduleByGroup(selectedGroup.value)

</script>