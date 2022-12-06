from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class AddTaskState(StatesGroup):
    date_user = State()
    task = State()
    category = State()


class ToMenusState(StatesGroup):
    main_menu = State()
    del_menu = State()


class ShowTaskState(StatesGroup):
    date_show_user = State()


class DelTaskState(StatesGroup):
    del_date_user = State()
    del_all_perm = State()
    get_date_user = State()
    get_number_user = State()


class AddNoteState(StatesGroup):
    add_note = State()
