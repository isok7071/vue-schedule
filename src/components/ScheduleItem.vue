<template>
    <v-col>
        <v-card
            v-for="dayId, day in  schedule "
            :key="dayId"
            height="100%"
            class="pt-4 rounded-lg"
        >
            <v-card-title class="text-primary">{{ day }}</v-card-title>
            <template
                v-for="groupRasp, group in  dayId "
                :key="group"
            >
                <ol>
                    <template
                        v-for="para, paraId in  groupRasp "
                        :key="paraId"
                    >
                        <v-card-text
                            class="ml-3"
                            v-if="!para"
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

<script lang="ts" setup>
defineProps<{
    schedule: {},
}>()
</script>