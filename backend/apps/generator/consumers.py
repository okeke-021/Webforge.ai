from channels.generic.websocket import AsyncJsonWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class ProjectConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for real-time project generation updates
    """
    
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = f'project_{self.project_id}'
        
        # Join project group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"WebSocket connected for project {self.project_id}")
    
    async def disconnect(self, close_code):
        # Leave project group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected for project {self.project_id}")
    
    async def receive_json(self, content):
        """
        Receive message from WebSocket
        """
        message_type = content.get('type')
        
        if message_type == 'join':
            # Client joined, send confirmation
            await self.send_json({
                'type': 'connected',
                'project_id': self.project_id
            })
    
    async def generation_status(self, event):
        """
        Send generation status update to WebSocket
        """
        await self.send_json({
            'type': 'generation_status',
            'status': event['status'],
            'progress': event['progress'],
            'message': event['message'],
            'msg_type': event.get('msg_type', 'info')
        })
    
    async def generation_complete(self, event):
        """
        Send generation complete message to WebSocket
        """
        await self.send_json({
            'type': 'generation_complete',
            'project_id': event['project_id'],
            'github_url': event.get('github_url'),
            'files_count': event.get('files_count'),
            'duration': event.get('duration')
        })
    
    async def generation_error(self, event):
        """
        Send generation error to WebSocket
        """
        await self.send_json({
            'type': 'generation_error',
            'error': event['error']
        })
