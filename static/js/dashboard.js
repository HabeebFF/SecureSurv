// Detection activity chart

const ctx1 = document.getElementById('activityChart');

new Chart(ctx1,{
type:'line',
data:{
labels:['08:00','09:00','10:00','11:00','12:00','13:00'],
datasets:[{
label:'Detections',
data:[12,28,45,37,52,41],
borderColor:'#3b82f6',
backgroundColor:'transparent'
}]
}
});


// Detections per camera

const ctx2 = document.getElementById('cameraChart');

new Chart(ctx2,{
type:'bar',
data:{
labels:['CAM-01','CAM-02','CAM-03','CAM-04'],
datasets:[{
label:'Detections',
data:[42,30,56,25],
backgroundColor:'#2563eb'
}]
}
});


// Known vs unknown

const ctx3 = document.getElementById('faceChart');

new Chart(ctx3,{
type:'doughnut',
data:{
labels:['Known','Unknown'],
datasets:[{
data:[75,25],
backgroundColor:['#3b82f6','#ef4444']
}]
}
});