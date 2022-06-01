from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin

from account.models import User, Comment
from .serializers import UserSerializer, CommentSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)

class UserConsumer(
        ListModelMixin,
        RetrieveModelMixin,
        PatchModelMixin,
        UpdateModelMixin,
        CreateModelMixin,
        DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserConsumerObserver(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    async def accept(self, **kwargs):
        await super().accept()
        await self.model_change.subscribe()

    @model_observer(User)
    async def model_change(self, message, **kwargs):
        await self.send_json(message)

class MyConsumer(GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    print('1', )

    @model_observer(Comment)
    async def comment_activity(
        self,
        message: CommentSerializer,
        observer=None,
        subscribing_request_ids=[],
        **kwargs
    ):
        print('2', message)
        await self.send_json(message.data)

    print('3')
    @comment_activity.serializer
    def comment_activity(self, instance: Comment, action, **kwargs) -> CommentSerializer:
        '''This will return the comment serializer'''
        print('4')
        return CommentSerializer(instance)

    @action()
    async def subscribe_to_comment_activity(self, request_id, **kwargs):
        print('5', kwargs)
        await self.comment_activity.subscribe(request_id=request_id)
        print('6',  )

    print('7')